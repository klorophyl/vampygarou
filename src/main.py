# coding: utf-8

import argparse
import socket
import struct

from vampygarou import Vampygarou, Map
from message import vampygarou_msg


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


class Server:
    """
    Main game server
    """

    def __init__(self, address, port):
        """
        Create a connection to the server
        """
        self.address = address
        self.port = port

        print "Connecting to {}:{}...".format(self.address, self.port)

        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self._sock.connect((server_address, server_port))
            print "- Connection established"
        except Exception as e:
            raise Exception("Couldn't connect to server: {}".format(e))

    def send_team_name(self):
        name = "vampygarou"
        print "Sending team name..."
        self._send_message("NME", len(name), name)
        print "- Team name sent"

    def get_order(self):
        return self.get_message(3)

    def get_messages_int(self, message_count):
        if message_count == 1:
            return struct.unpack('=B', self.get_message(1))[0]
        else:
            return [struct.unpack('=B', self.get_message(1))[0] for _ in range(message_count)]

    def get_message(self, size):
        try:
            message = self._sock.recv(size)
            return message
        except Exception as e:
            raise Exception("Couldn't receive message: {}".format(e))

        return None

    def send_move(self, *args):
        self._send_message("MOV", *args)

    def close(self):
        self._sock.close()

    def _send_message(self, *messages):
        """
        Send a given set of messages to the server
        """
        for message in messages:
            try:
                data = struct.pack('=B', message) if isinstance(message, int) else message
                self._sock.send(data)
            except:
                raise Exception("Couldn't send message: {}".format(message))


def get_map_size():
    print "Getting map size"
    ligns, columns = server.get_messages_int(2)
    print "- Map size: {},{}".format(ligns, columns)
    game_map = Map(ligns, columns)
    print game_map


def get_houses():
    print "Getting houses"
    n = server.get_messages_int(1)
    houses = []
    for i in range(n):
        x, y = server.get_messages_int(2)
        houses.append([x, y])
    print "- Houses: {}".format(houses)


def get_home():
    print "Getting starting point"
    home_x, home_y = server.get_messages_int(2)
    print "- Home: {}".format([home_x, home_y])


def update_moves():
    print "Entering update"
    n = server.get_messages_int(1)
    changes = []
    for i in range(n):
        changes.append(server.get_messages_int(5))
        print "- Changes: {}".format(changes[-1])
    # mettez à jour votre carte à partir des tuples contenus dans changes
    # calculez votre coup
    # préparez la trame MOV ou ATK
    # Par exemple:
    for moves in vampygarou.get_moves():
        server.send_move(*moves)


def update_map():
    print "Getting map"
    n = server.get_messages_int(1)
    changes = []
    for i in range(n):
        changes.append(server.get_messages_int(5))
        print "- Changes: {}".format(changes[-1])
    # initialisez votre carte à partir des tuples contenus dans changes


def end_game():
    print "End of game"
    # ici on met fin à la partie en cours
    # Réinitialisez votre modèle


def run_game():
    order = server.get_order()

    if order == "SET":
        get_map_size()
    elif order == "HUM":
        get_houses()
    elif order == u"HME":
        get_home()
    elif order == "UPD":
        update_moves()
    elif order == "MAP":
        update_map()
    elif order == "END":
        end_game()
    elif order == "BYE":
        print "Quitting"
        print "Bye bye!"
        return False
    elif len(order) > 0:
        print "- Unknown command: {}".format(list(bytes(order)))

    return True


if __name__ == "__main__":
    print vampygarou_msg

    args = parse_args()
    if args.name:
        print "\n\t\tBonjour {name}, je suis Vampygarou.\n\n".format(name=args.name.capitalize())

    vampygarou = Vampygarou(args.manual)

    server_address = args.ip or "192.168.56.101"
    server_port = args.port or 5555

    server = Server(server_address, server_port)
    server.send_team_name()

    running = True
    while running:
        running = run_game()

    server.close()
