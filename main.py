#!/usr/bin/env python3

import argparse
import logging
import re
import time
import threading
from pythonosc import dispatcher
from pythonosc import osc_server

from lights import FrameBuffer, decode_rgba32
from lights.device_neopixels import NeoPixels

logging.basicConfig(level=logging.DEBUG,
                    format='%(levelname)8s (%(threadName)-10s) %(message)s',
                    )

# Light Config

parser = argparse.ArgumentParser()
parser.add_argument("--ip",
                    default="0.0.0.0", help="The ip to listen on")
parser.add_argument("--port",
                    type=int, default=5005, help="The port to listen on")
args = parser.parse_args()

neo_pixels = NeoPixels("grid", 32)


def do_color(addr, color):

    cord = re.search("/light/(\d+)/(\d+)/color", addr)

    red, green, blue, alpha = decode_rgba32(color)

    i = int(cord.group(1)) + int(cord.group(2)) * 8

    neo_pixels.set(red, green, blue, i)
    neo_pixels.show()


dispatch = dispatcher.Dispatcher()
dispatch.map("/light/*/*/color", do_color)

server = osc_server.ThreadingOSCUDPServer(
    (args.ip, args.port), dispatch)
print("Serving on {}".format(server.server_address))
server.serve_forever()
