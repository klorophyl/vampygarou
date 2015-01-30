# coding: utf-8
import socket
import struct


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
            self._sock.connect((self.address, self.port))
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
