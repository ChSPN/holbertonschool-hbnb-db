import os
import threading
import time

from utils.constants import REPOSITORY_ENV_VAR
from src import create_app
from werkzeug.serving import make_server
from tests.run_all import main

app = create_app()


class ServerThread(threading.Thread):
    def __init__(self, app):
        threading.Thread.__init__(self)
        self.srv = make_server("127.0.0.1", 5000, app)
        self.ctx = app.app_context()
        self.ctx.push()

    def run(self):
        self.srv.serve_forever()

    def shutdown(self):
        self.srv.shutdown()


if __name__ == "__main__":
    os.environ[REPOSITORY_ENV_VAR] = "file"
    mon_thread = ServerThread(app)
    mon_thread.start()
    time.sleep(2)
    main()
    mon_thread.shutdown()
    os.environ[REPOSITORY_ENV_VAR] = "db"
    mon_thread = ServerThread(app)
    mon_thread.start()
    time.sleep(2)
    main()
    mon_thread.shutdown()
