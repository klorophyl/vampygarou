# coding: utf-8

import argparse
import socket
import struct

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

        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self._sock.connect((server_address, server_port))
        except Exception as e:
            raise Exception("Couldn't connect to server: {}".format(e))

    def send_team_name(self):
        name = "vampygarou"
        self._send_message("NME", len(name), name)

    def get_order(self):
        return self.get_message(3)

    def get_messages_int(self, message_count, size=1):
        if message_count == 1:
            return struct.unpack('=B', self.get_message(size))[0]
        else:
            return (struct.unpack('=B', self.get_message(size))[0] for _ in range(message_count))

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


if __name__ == "__main__":
    print vampygarou_msg

    args = parse_args()

    if args.name:
        print "\n\t\tBonjour {name}, je suis Vampygarou.\n\n".format(name=args.name.capitalize())

    server_address = args.ip or "192.168.56.101"
    server_port = args.port or 5555

    print "Connecting to {}:{}...".format(server_address, server_port)
    server = Server(server_address, server_port)
    print "Connection established"

    print "Sending team name..."
    server.send_team_name()
    print "Team name sent"

    # main loop
    while True:
        print "Getting order"
        order = server.get_order()
        print order

        if order == "SET":
            lignes, colonnes = server.get_messages_int(2)
            # ici faire ce qu'il faut pour préparer votre représentation
            # de la carte
        elif order == "HUM":
            n = server.get_messages_int(1)
            maisons = []
            for i in range(n):
                maisons.append(server.get_messages_int(2))
            # maisons contient la liste des coordonnées des maisons
            # ajoutez votre code ici
        elif order == "HME":
            x, y = server.get_messages_int(2)
            # ajoutez le code ici (x,y) étant les coordonnées de votre
            # maison
        elif order == "UPD":
            n = server.get_messages_int(1)
            changes = []
            for i in range(n):
                changes.append(server.get_messages_int(5))
            # mettez à jour votre carte à partir des tuples contenus dans changes
            # calculez votre coup
            # préparez la trame MOV ou ATK
            # Par exemple:
            server.send_move(1, 2, 1, 1, 3)
        elif order == "MAP":
            n = server.get_messages_int(1)
            changes = []
            for i in range(n):
                changes.append(server.get_messages_int(5))
            # initialisez votre carte à partir des tuples contenus dans changes
        elif order == "END":
            pass
            # ici on met fin à la partie en cours
            # Réinitialisez votre modèle
        elif order == "BYE":
            break
        else:
            print "Commande non attendue recue :", order

    server.close()
