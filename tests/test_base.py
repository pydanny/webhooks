from subprocess import Popen
from test_server import app


def start_test_server():
    app.user_reloader = False
    test_server = Popen(["python", "test_server.py"])
    return test_server

def end_test_server(test_server):
    test_server.terminate()
