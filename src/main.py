# coding: utf-8
import argparse
import os
import time
import sys
import traceback
import pdb

from server import Server
from vampygarou import Vampygarou
from mapping import Map
from message import vampygarou_msg, Colors


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-name",
        help="the team name",
        type=str
    )
    parser.add_argument(
        "-port",
        help="the server port",
        type=int
    )
    parser.add_argument(
        "-ip",
        help="the server address",
        type=str
    )
    parser.add_argument(
        "-manual",
        help="player is human",
        dest="manual",
        action="store_true"
    )
    parser.add_argument(
        "-random",
        help="play randomly",
        dest="random",
        action="store_true"
    )
    parser.add_argument(
        "-bourrin",
        help="play like a bourrin",
        dest="bourrin",
        action="store_true"
    )
    parser.set_defaults(manual=False)

    return parser.parse_args()


def get_map_size(vampygarou):
    print "Getting map size"
    ligns, columns = server.get_messages_int(2)
    print "- Map size: {},{}".format(columns, ligns)
    vampygarou.map = Map(columns, ligns)


def get_houses(vampygarou):
    print "Getting houses"
    n = server.get_messages_int(1)
    for i in range(n):
        x, y = server.get_messages_int(2)
        # vampygarou.map.add_house(x, y)
    print "- Got {} houses".format(n)


def get_home(vampygarou):
    print "Getting starting point"
    x, y = server.get_messages_int(2)
    vampygarou.map.set_home(x, y)
    print "- Home: {}".format([x, y])


def update_moves(vampygarou):
    update_map(vampygarou)
    server.send_moves(vampygarou.get_moves())


def update_map(vampygarou):
    print "Getting map"
    n = server.get_messages_int(1)
    changes = []
    for i in range(n):
        changes.append(server.get_messages_int(5))
    vampygarou.map.update_with_changes(changes)


def end_game(vampygarou):
    print "End of game"


def run_game(vampygarou):
    order = server.get_order()

    if order == "SET":
        get_map_size(vampygarou)
    elif order == "HUM":
        get_houses(vampygarou)
    elif order == u"HME":
        get_home(vampygarou)
    elif order == "UPD":
        update_moves(vampygarou)
        print vampygarou.map
    elif order == "MAP":
        update_map(vampygarou)
        if vampygarou.race is None:
            vampygarou.retrieve_race()
        print vampygarou.map
    elif order == "END":
        end_game(vampygarou)
    elif order == "BYE":
        print "Quitting"
        print "Bye bye!"
        return False
    elif len(order) > 0:
        print "- Unknown command: {}".format(list(bytes(order)))

    return True


if __name__ == "__main__":
    print vampygarou_msg

    if os.name == "nt":
        Colors.disable()

    args = parse_args()

    name = args.name or "Vampygarou"
    print "\n\t\tBonjour {}, je suis Vampygarou.\n\n".format(name)

    vampygarou = Vampygarou(name, args.manual, args.random, args.bourrin)

    server_address = args.ip or "127.0.0.1"
    server_port = args.port or 5555

    server = Server(server_address, server_port)
    server.send_team_name(vampygarou.name)

    running = True
    while running:
        running = run_game(vampygarou)

    server.close()
