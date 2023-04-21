import hou
import os
import hwebserver
import sys
import getopt
from lib import logo
from lib import serializer
from lib import api


def print_help_info():
    print("Usage: hython harpoon.py [-p port (default:80)]")
    print("Options:")
    print("-?,-h    : this help")
    print("-d       : run in debug mode")
    print("-p       : specify server port")
    print("-s       : specify static files directory")


def setupEnv():
    HARPOON_ROOT = os.path.dirname(os.path.abspath(sys.argv[0]))
    print(HARPOON_ROOT)
    hou.putenv("HARPOON_ROOT", HARPOON_ROOT)


if __name__ == "__main__":
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
        elif opt in ("-s", "--static"):
            hwebserver.registerStaticFilesDirectory(
                arg,
                "/static")
    max_upload_size = 1024*1024*1024*1024
    setupEnv()
    hwebserver.run(port, debug, max_in_memory_file_upload_size=max_upload_size, max_request_size=max_upload_size)
