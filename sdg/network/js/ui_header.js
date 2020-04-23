
const maxRecursion = 50;

let _nodeDepencies = {};

let _networkInvocations = {};
function updateAndCheckCalls(networkInvocationId, callable) {
  // check excessive recursion
  let current = _networkInvocations[networkInvocationId];
  if (current === undefined) {
    let obj = { _time: Date.now() };
    _networkInvocations[callable] = obj;
    obj[callable] = 1;
    return false;
  }

  if ((current._time + 1000) > Date.now()) {
    // reset after one second
    let obj = { _time: Date.now() };
    _networkInvocations[callable] = obj;
    obj[callable] = 1;
    return false;
  } else {
    const count = current[callable];
    current['_time'] = Date.now();
    if (count === undefined) {
      // have not seen this node
      current[callable] = 1;
      return false;
    } else if (count > maxRecursion) {
      // too much recursion
      throw "Too much recursion";
      return true;
    } else {
      // increment call count
      current[callable] = count + 1;
    }
  }

  return false;
}

// https://github.com/getify/TNG-Hooks
// NOTE: both `guards1` and `guards2` are either
//    `undefined` or an array
function guardsChanged(guards1,guards2) {
  // either guards list not set?
  if (guards1 === undefined || guards2 === undefined) {
    // force assumption of change in guards
    return true;
  }

  // guards lists of different length?
  if (guards1.length !== guards2.length) {
    // guards changed
    return true;
  }

  // check guards lists for differences
  //    (only shallow value comparisons)
  for (let [idx,guard] of guards1.entries()) {
    if (!Object.is(guard,guards2[idx])) {
      // guards changed
      return true;
    }
  }

  // assume no change in guards
  return false;
}


function allowCallAndChanged(prev, current) {
  return guardsChanged(prev, current);
}


function arrayNoNulls(arr) {
  for (let i = 0; i < arr.length; i++) {
    if (arr[i] === null || arr[i] === undefined) {
      return false;
    }
  }
  return true;
}