from subprocess import Popen
from test_server import app
import logging
import sys


def start_test_server():
    app.user_reloader = False
    test_server = Popen(["python", "test_server.py"])
    return test_server

def end_test_server(test_server):
    test_server.terminate()

def configure_debug_logging():
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)