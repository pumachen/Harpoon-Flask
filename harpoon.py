import os
import sys
import signal
import getopt
import hou
from flask import Flask, request
from lib import logo
from lib import api

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

@app.route("/api/hdalibrary", methods=['GET'])
def hdalibrary():
    return api.hdalibrary(request)

@app.route("/api/hdaprocessor/<hda_name>", methods=['GET', 'POST'])
def hdaprocessor(hda_name):
    return api.hdaprocessor(hda_name, request)

@app.route("/api/hiplibrary", methods=['GET'])
def hiplibrary():
    return api.hiplibrary(request)

@app.route("/api/hipprocessor/<hip_name>", methods=['GET', 'POST'])
def hipprocessor(hip_name):
    return api.hipprocessor(hip_name, request)

@app.route("/api/torlibrary", methods=['GET'])
def torlibrary():
    return api.torlibrary(request)

@app.route("/api/torprocessor/<tor_file>", methods=['GET', 'POST'])
def torprocessor(tor_file):
    return api.torprocessor(tor_file, request)

def print_help_info():
    print("Usage: hython harpoon.py [-p port (default:80)]")
    print("Options:")
    print("-?,-h    : this help")
    print("-d       : run in debug mode")
    print("-p       : specify server port")
    # print("-s       : specify static files directory")


def on_exit(signal, frame):
    print('Bye!')
    sys.exit(0)


if __name__ == '__main__':
    port = 80
    debug = False
    opts, args = getopt.getopt(sys.argv[1:], "hdp:s:", ["port=", "help", "debug", "static"])
    for opt, arg in opts:
        if opt in ("-h", "--help", "-?"):
            print_help_info()
            sys.exit()
        elif opt in ("-d", "--debug"):
            debug = True
        elif opt in ("-p", "--port"):
            port = int(arg)
    signal.signal(signal.SIGINT, on_exit)
    app.run(host = "0.0.0.0", port = port, debug = debug)
