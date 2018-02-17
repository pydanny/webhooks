from subprocess import Popen
from tests.server_test import app
import logging
import sys
import os


def start_test_server():
    app.user_reloader = False
    test_server = Popen(["python", os.path.join(os.path.dirname(__file__), "server_test.py")])
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