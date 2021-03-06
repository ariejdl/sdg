
# TODO: add terminal
# https://github.com/jupyter/notebook/blob/master/notebook/terminal/__init__.py
# https://github.com/jupyter/notebook/blob/master/notebook/terminal/handlers.py#L14
# https://github.com/jupyter/notebook/blob/notebook/terminal/api_handlers.py#L29

import os

import terminado
from notebook.utils import check_version

if not check_version(terminado.__version__, '0.8.1'):
    raise ImportError("terminado >= 0.8.1 required, found %s" % terminado.__version__)

from ipython_genutils.py3compat import which
from terminado import NamedTermManager
from tornado.log import app_log
from notebook.utils import url_path_join as ujoin
from notebook.terminal import TermSocket
from notebook.terminal import api_handlers

class _TermSocket(TermSocket):

    def check_origin(self, origin):
        # enable CORS, check security! check if overriden by allow_origin='*'
        return True

# slightly modified, no html page route
def initialize(webapp, notebook_dir, connection_url, settings):
    if os.name == 'nt':
        default_shell = 'powershell.exe'
    else:
        default_shell = which('sh')
    shell = settings.get('shell_command',
        [os.environ.get('SHELL') or default_shell]
    )
    # Enable login mode - to automatically source the /etc/profile script
    if os.name != 'nt':
        shell.append('-l')
    terminal_manager = webapp.settings['terminal_manager'] = NamedTermManager(
        shell_command=shell,
        extra_env={ 'SDG_SERVER_URL': connection_url }
    )
    terminal_manager.log = app_log
    base_url = webapp.settings['base_url']
    handlers = [
        (ujoin(base_url, r"/terminals/websocket/(\w+)"), _TermSocket,
             {'term_manager': terminal_manager}),
        (ujoin(base_url, r"/api/terminals"), api_handlers.TerminalRootHandler),
        (ujoin(base_url, r"/api/terminals/(\w+)"), api_handlers.TerminalHandler),
    ]
    webapp.add_handlers(".*$", handlers)
