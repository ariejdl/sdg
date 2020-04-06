
import pytest

from sdg.network.network import Network
from sdg.network.nodes import Node, create_node
from sdg.network.edges import Edge, create_edge

DEFAULT_TEST_NODE = 'py_rest_node'
DEFAULT_TEST_EDGE = 'rest_edge'

def test_basic():
    nw = Network()
    
    n1 = Node({'a': 1})
    n2 = Node({'b': 1})

    e1 = Edge({'c': 1})
    e2 = Edge({'d': 1})

    n1_s = n1.serialize(1)
    n2_s = n2.serialize(2)
    
    assert n1_s['id'] == 1
    assert n1_s['model']['a'] == 1
    assert n1_s['model'].get('b') == None

    assert n2_s['id'] == 2
    assert n2_s['model']['b'] == 1
    assert n2_s['model'].get('c') == None

    nws = nw.serialize()
    assert nws['nodes'] == []
    assert nws['edges'] == []
    assert nws['network'] == {}

    n1 = create_node({ 'x': 100 }, type=DEFAULT_TEST_NODE)
    n1_s = n1.serialize(10)
    assert n1_s['id'] == 10
    assert n1_s['model']['x'] == 100
    assert n1_s['type'] == DEFAULT_TEST_NODE

    with pytest.raises(Exception):
        n1 = create_node({ 'x': 100 }, type='py_rest_node_***')


def test_network():
    nw = Network({
        'network': {},
        'nodes': [],
        'edges': []
    })

    nw.add_node(_id=1, model={ 'x': 1 }, type=DEFAULT_TEST_NODE)
    nw.add_node(_id=2, model={ 'x': 2 }, type=DEFAULT_TEST_NODE)
    nw.add_node(_id=3, model={ 'y': 1 }, type=DEFAULT_TEST_NODE)

    nw.add_edge(1, 2, model={ 'z': 1 }, type=DEFAULT_TEST_EDGE)
    nw.add_edge(1, 3, model={ 'z': 2 }, type=DEFAULT_TEST_EDGE)

    with pytest.raises(Exception):
        nw.add_node(_id=1, model={ 'x': 1 }, type=DEFAULT_TEST_NODE)

    with pytest.raises(Exception):
        nw.add_edge(1, 3, model={ 'z': 2 }, type=DEFAULT_TEST_EDGE)
        
    ser = nw.serialize()

    assert ser['network'][1] == [2,3]
    assert ser['network'][2] == [1]
    assert ser['network'][3] == [1]

    assert len(ser['nodes']) == 3
    assert ([n for n in ser['nodes'] if n['id'] == 2])[0]['model'] == {'x': 2}

    assert len(ser['edges']) == 2
    
