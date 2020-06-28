
import os
import sys
import tornado
import logging as log

log.basicConfig(stream=sys.stdout, level=log.DEBUG)

from notebook.services.contents.filemanager import FileContentsManager

from ..network.network import NetworkManager
from .terminal_handlers import initialize as init_terminal
from .kernel_handlers import handlers as kernel_handlers
from .contents_handlers import handlers as contents_handlers

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("""
        <!DOCTYPE html>
        <html>
          <head>

            <link rel="stylesheet" href="/static/style.css?q=1" />
            <script src="/static/app.bundle.js?q=1"></script>

          </head>
          <body>
          </body>
        </html>
        """)


class WSEchoHandler(tornado.websocket.WebSocketHandler):

    def open(self):
        pass

    def on_message(self, message):
        self.write_message(u"You said: " + message)

    def on_close(self):
        pass


def main():
    port = 8001
    server_url = 'http://localhost:{}'.format(port)

    cur_dir = os.path.abspath(os.getcwd())

    settings = {
        "static_path": os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..', '..', 'client', 'dist')),
        # TODO: implement
        "login_url": "/login",
        "base_url": "/",
        "contents_manager": FileContentsManager(),
        "network_manager": NetworkManager()
    }
    
    application = tornado.web.Application([
        (r"/", MainHandler),
        (r"/echo", WSEchoHandler),

        *kernel_handlers,
        *contents_handlers
        
    ], **settings)

    init_terminal(application, cur_dir, server_url, settings)

    log.info("listening on {}".format(port))
    application.listen(port)
    tornado.ioloop.IOLoop.current().start()

