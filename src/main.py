# coding: utf-8
import argparse
import os

from server import Server
from vampygarou import Vampygarou
from mapping import Map
from message import vampygarou_msg, Colors


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-name",
        help="display a message for you",
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
        vampygarou.map.add_house(x, y)
    print "- Got {} houses".format(n)


def get_home(vampygarou):
    print "Getting starting point"
    x, y = server.get_messages_int(2)
    vampygarou.map.set_home(x, y)
    print "- Home: {}".format([x, y])


def update_moves(vampygarou):
    print "Entering update"
    n = server.get_messages_int(1)
    changes = []
    for i in range(n):
        changes.append(server.get_messages_int(5))
        print "- Changes: {}".format(changes[-1])

    server.send_moves(*vampygarou.get_moves())


def update_map(vampygarou):
    print "Getting map"
    n = server.get_messages_int(1)
    changes = []
    for i in range(n):
        changes.append(server.get_messages_int(5))
        print "- Changes: {}".format(changes[-1])

    vampygarou.map.init_counts(changes)


def end_game(vampygarou):
    print "End of game"
    # ici on met fin à la partie en cours
    # Réinitialisez votre modèle


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
    elif order == "MAP":
        update_map(vampygarou)
    elif order == "END":
        end_game(vampygarou)
    elif order == "BYE":
        print "Quitting"
        print "Bye bye!"
        return False
    elif len(order) > 0:
        print "- Unknown command: {}".format(list(bytes(order)))

    print vampygarou.map

    return True


if __name__ == "__main__":
    print vampygarou_msg

    if os.name == "nt":
        Colors.disable()

    args = parse_args()
    if args.name:
        print "\n\t\tBonjour {name}, je suis Vampygarou.\n\n".format(name=args.name.capitalize())

    vampygarou = Vampygarou(args.manual)

    server_address = args.ip or "127.0.0.1"
    server_port = args.port or 5555

    server = Server(server_address, server_port)
    server.send_team_name()

    running = True
    while running:
        running = run_game(vampygarou)

    server.close()
