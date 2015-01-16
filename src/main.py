# coding: utf-8

import socket, struct


def send(sock, *messages):
    """Send a given set of messages to the server."""
    for message in messages:
        try:
            data = struct.pack('=B', message) if isinstance(message, int) else message
            sock.send(data)
        except:
            print "Couldn't send message: ", message



#Création de la socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Connexion de la socket
try:
    sock.connect(("127.0.0.1", 5555)) #Changez ici l'adresse ip et le port
except IOError as error:
    print "Connection error: ", error

#Envoi du nom
groupname = "vampygarou" #mettez ici le nom de votre équipe
send(sock, "NME", len(groupname), groupname)


#boucle principale
while True:
    try:
        order = sock.recv(3)
    except Exception as e:
        print "Error: ", e

    if order == "SET":
        lignes, colonnes = (struct.unpack('=B', self._s.recv(1))[0] for i in range(2))
        #ici faire ce qu'il faut pour préparer votre représentation
        #de la carte
    elif order == "HUM":
        n = struct.unpack('=B', self._s.recv(1))[0]
        maisons = []
        for i in range(n):
            maisons.append((struct.unpack('=B', self._s.recv(1))[0] for i in range(2)))
        #maisons contient la liste des coordonnées des maisons
        #ajoutez votre code ici
    elif order == "HME":
        x, y = (struct.unpack('=B', self._s.recv(1))[0] for i in range(2))
        #ajoutez le code ici (x,y) étant les coordonnées de votre
        #maison
    elif order == "UPD":
        n = struct.unpack('=B', self._s.recv(1))[0]
        changes = []
        for i in range(n):
            changes.append((struct.unpack('=B', self._s.recv(1))[0] for i in range(5)))
        #mettez à jour votre carte à partir des tuples contenus dans changes
        #calculez votre coup
        #préparez la trame MOV ou ATK
        #Par exemple:
        send(sock, "MOV", 1,2,1,1,3)
    elif order == "MAP":
        n = struct.unpack('=B', self._s.recv(1))[0]
        changes = []
        for i in range(n):
            changes.append((struct.unpack('=B', self._s.recv(1))[0] for i in range(5)))
        #initialisez votre carte à partir des tuples contenus dans changes
    elif order == "END":
        pass
        #ici on met fin à la partie en cours
        #Réinitialisez votre modèle
    elif order == "BYE":
        break
    else:
        print "Commande non attendue recue :", order

#Préparez ici la déconnexion

#Fermeture de la socket
    sock.close()






