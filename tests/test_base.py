from subprocess import Popen
from tests.test_server import app
import logging
import sys
import os


def start_test_server():
    app.user_reloader = False
    test_server = Popen(["python", os.path.join(os.path.dirname(__file__), "test_server.py")])
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