import socket
import select
import sys
from PyQt5 import *
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QPlainTextEdit, QPlainTextDocumentLayout

HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = 54005
BUFFER_SIZE = 1024
numClients = 0


def receive_message(client_socket):
    try:
        # Receive our "header" containing message length, it's size is defined and constant
        message_header = client_socket.recv(HEADER_LENGTH)

        # If we received no data, client gracefully closed a connection, for example using socket.close() or socket.shutdown(socket.SHUT_RDWR)
        if not len(message_header):
            return False

        # Convert header to int value
        message_length = int(message_header.decode('utf-8').strip())

        # Return an object of message header and message data
        return {'header': message_header, 'data': client_socket.recv(message_length)}
    except:
        return False


class Server_Main(QtWidgets.QMainWindow):
    def __init__(self):
        global numClients
        super(Server_Main, self).__init__()  # Call the inherited classes __init__ method
        uic.loadUi('ScreenServer_Main.ui', self)  # Load the .ui file
        numClients = int(self.lineEditNumClient.text())
        self.pushButtonOpenServer.clicked.connect(self.gotoOpenServer)
        # self.pushButtonCloseServer.clicked.connect(self.gotoCloseServer)
        # data = f'Listening for connections on {IP}:{PORT}...'
        # self.plainTextEdit.setPlainText("Helo")
        # self.plainTextEdit.insertPlainText("Phuoc\n")
        # self.pushButtonCloseServer.clicked.connect(self.gotoCloseServer)

    def gotoCloseServer(self):
        return

    def gotoOpenServer(self):
        countClients = 0
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((IP, PORT))
        server_socket.listen()
        sockets_list = [server_socket]
        clientsUser = {}
        print(f'Listening for connections on {IP}:{PORT}...')

        def Func_VIEW(client_socket):
            ID_Book = receive_message(client_socket)
            Book = ID_Book['data'].decode('utf-8')
            Book += ".txt"
            check = False

            try:
                open(Book)
            except IOError:
                messExit = "EXIT"
                messExit = messExit.encode('utf-8')
                messExit_header = f"{len(messExit):<{HEADER_LENGTH}}".encode('utf-8')
                client_socket.send(messExit_header + messExit)
                return

            with open(Book, "r") as f:
                lines = f.read()
                messData = lines
                messData1 = messData.encode('utf-8')
                messData_header = f"{len(messData1):<{HEADER_LENGTH}}".encode('utf-8')
                client_socket.send(messData_header + messData1)
                check = True
                f.close()
            return

        def Func_DOWNLOAD(client_socket):
            ID_Book = receive_message(client_socket)

            with open("InforBook.txt", "r") as f:
                lines = f.readlines()
                line = 0
                while line < len(lines):
                    s = lines[line].strip("\n").split(", ")
                    if ID_Book['data'].decode() == s[0]:
                        filename = s[5]
                        addressfile = filename.encode('utf-8')
                        addressfile_header = f"{len(addressfile):<{HEADER_LENGTH}}".encode('utf-8')
                        client_socket.send(addressfile_header + addressfile)
                        with open(filename, "rb") as f1:
                            fullfile = f1.read()
                            messData = fullfile
                            messData_header = f"{len(messData):<{HEADER_LENGTH}}".encode('utf-8')
                            client_socket.send(messData_header + messData)
                            f1.close()
                            f.close()
                            return
                    line += 1
                messExit = "EXIT"
                messExit = messExit.encode('utf-8')
                messExit_header = f"{len(messExit):<{HEADER_LENGTH}}".encode('utf-8')
                client_socket.send(messExit_header + messExit)
                client_socket.send(messExit_header + messExit)
                f.close()
                return

        def Func_Find_ID(client_socket):
            ID = message['data'].decode('utf-8')[5:8]

            with open("InforBook.txt", "r") as f:
                lines = f.readlines()
                line = 0
                while line < len(lines):
                    checkType = lines[line].strip("\n").split(", ")
                    if ID == checkType[0]:
                        messData = lines[line].strip("\n")
                        messData1 = messData.encode('utf-8')
                        messData_header = f"{len(messData1):<{HEADER_LENGTH}}".encode('utf-8')
                        client_socket.send(messData_header + messData1)
                    line += 1
                messExit = "EXIT"
                messExit = messExit.encode('utf-8')
                messExit_header = f"{len(messExit):<{HEADER_LENGTH}}".encode('utf-8')
                client_socket.send(messExit_header + messExit)
                f.close()
                return

        def Func_Find_Name(client_socket):
            Name = message['data'].decode('utf-8')[7:]
            with open("InforBook.txt", "r") as f:
                lines = f.readlines()
                line = 0
                while line < len(lines):
                    checkType = lines[line].strip("\n").split(", ")
                    if Name == checkType[1]:
                        messData = lines[line].strip("\n")
                        messData1 = messData.encode('utf-8')
                        messData_header = f"{len(messData1):<{HEADER_LENGTH}}".encode('utf-8')
                        client_socket.send(messData_header + messData1)
                    line += 1
                messExit = "EXIT"
                messExit = messExit.encode('utf-8')
                messExit_header = f"{len(messExit):<{HEADER_LENGTH}}".encode('utf-8')
                client_socket.send(messExit_header + messExit)
                f.close()
                return

        def Func_Find_Type(client_socket):
            Type = message['data'].decode('utf-8')[7:]

            with open("InforBook.txt", "r") as f:
                lines = f.readlines()
                line = 0
                while line < len(lines):
                    checkType = lines[line].strip("\n").split(", ")
                    if Type == checkType[2]:
                        messData = lines[line].strip("\n")
                        messData1 = messData.encode('utf-8')
                        messData_header = f"{len(messData1):<{HEADER_LENGTH}}".encode('utf-8')
                        client_socket.send(messData_header + messData1)
                    line += 1
                messExit = "EXIT"
                messExit = messExit.encode('utf-8')
                messExit_header = f"{len(messExit):<{HEADER_LENGTH}}".encode('utf-8')
                client_socket.send(messExit_header + messExit)
                f.close()
                return

        def Func_Find_Author(client_socket):
            Author = message['data'].decode('utf-8')[9:]

            with open("InforBook.txt", "r") as f:
                lines = f.readlines()
                line = 0
                while line < len(lines):
                    checkType = lines[line].strip("\n").split(", ")
                    if Author == checkType[3]:
                        messData = lines[line].strip("\n")
                        messData1 = messData.encode('utf-8')
                        messData_header = f"{len(messData1):<{HEADER_LENGTH}}".encode('utf-8')
                        client_socket.send(messData_header + messData1)
                    line += 1
                messExit = "EXIT"
                messExit = messExit.encode('utf-8')
                messExit_header = f"{len(messExit):<{HEADER_LENGTH}}".encode('utf-8')
                client_socket.send(messExit_header + messExit)
                f.close()
                return

        while True:
            read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

            # Iterate over notified sockets
            for notified_socket in read_sockets:
                # If notified socket is a server socket - new connection, accept it
                if notified_socket == server_socket:
                    # Accept new connection
                    # That gives us new socket - client socket, connected to this given client only, it's unique for that client
                    # The other returned object is ip/port set
                    client_socket, client_address = server_socket.accept()
                    # Client should send his name right away, receive it
                    User = receive_message(client_socket)
                    Pass = receive_message(client_socket)
                    Check = receive_message(client_socket)

                    if (User is False) or (Pass is False):
                        mess = "0"
                        mess = mess.encode('utf-8')
                        mess_header = f"{len(mess):<{HEADER_LENGTH}}".encode('utf-8')
                        client_socket.send(mess_header + mess)
                        continue

                    us = User['data'].decode('utf-8')
                    pa = Pass['data'].decode('utf-8')

                    if (Check['data'].decode('utf-8') == "SIGNUP"):
                        with open("Accounts.txt", "r") as f:
                            lines = f.readlines()
                            line = 0
                            while line < len(lines):
                                if lines[line].strip("\n") == us:
                                    mess = '0'.encode('utf-8')
                                    mess_header = f"{len(mess):<{HEADER_LENGTH}}".encode('utf-8')
                                    client_socket.send(mess_header + mess)
                                line += 2
                            if line >= len(lines):
                                mess = '1'.encode('utf-8')
                                mess_header = f"{len(mess):<{HEADER_LENGTH}}".encode('utf-8')
                                client_socket.send(mess_header + mess)
                                with open("Accounts.txt", "a") as f:
                                    f.writelines(f'\n{us}')
                                    f.writelines(f'\n{pa}')
                            f.close()
                        client_socket.close()
                        continue

                    else:
                        checkCorrect = False
                        with open("Accounts.txt", "r") as f:
                            lines = f.readlines()
                            line = 0
                            while line < len(lines):
                                if lines[line].strip("\n") == us and lines[line + 1].strip("\n") == pa:
                                    if countClients < numClients:
                                        f.close()
                                        print('Accepted new connection from {}:{}, username: {}'.format(*client_address,
                                                                                                        User[
                                                                                                            'data'].decode(
                                                                                                            'utf-8')))
                                        countClients += 1
                                        mess = "1"
                                        mess = mess.encode('utf-8')
                                        mess_header = f"{len(mess):<{HEADER_LENGTH}}".encode('utf-8')
                                        checkCorrect = True
                                        client_socket.send(mess_header + mess)
                                        # Add accepted socket to select.select() list
                                        sockets_list.append(client_socket)
                                        # Also save username and username header
                                        clientsUser[client_socket] = User
                                    else:
                                        print("Server is full")

                                line += 2
                            if checkCorrect == False:
                                f.close()
                                mess = "0"
                                mess = mess.encode('utf-8')
                                mess_header = f"{len(mess):<{HEADER_LENGTH}}".encode('utf-8')
                                client_socket.send(mess_header + mess)
                                continue

                # Else existing socket is sending a message
                else:
                    # Receive message
                    message = receive_message(notified_socket)

                    # If False, client disconnected, cleanup
                    if message is False:
                        print('Closed connection from: {}'.format(clientsUser[notified_socket]['data'].decode('utf-8')))
                        countClients -= 1

                        # Remove from list for socket.socket()
                        sockets_list.remove(notified_socket)

                        # Remove from our list of users
                        del clientsUser[notified_socket]
                        continue

                    # Get user by notified socket, so we will know who sent the message
                    user = clientsUser[notified_socket]
                    ####

                    if (message["data"].decode("utf-8") == "VIEW"):
                        Func_VIEW(notified_socket)
                    if (message["data"].decode("utf-8") == "DOWNLOAD"):
                        Func_DOWNLOAD(notified_socket)
                    if ("F_ID " in message["data"].decode("utf-8")):
                        Func_Find_ID(notified_socket)
                    if ("F_Name " in message["data"].decode("utf-8")):
                        Func_Find_Name(notified_socket)
                    if ("F_Type " in message["data"].decode("utf-8")):
                        Func_Find_Type(notified_socket)
                    if ("F_Author " in message["data"].decode("utf-8")):
                        Func_Find_Author(notified_socket)

                    ####
                    print(f'From Username "{user["data"].decode("utf-8")}" => {message["data"].decode("utf-8")}')

            # It's not really necessary to have this, but will handle some socket exceptions just in case
            for notified_socket in exception_sockets:
                # Remove from list for socket.socket()
                sockets_list.remove(notified_socket)

                # Remove from our list of users
                del clientsUser[notified_socket]


class Server_Show(QtWidgets.QMainWindow):
    def __init__(self, datatext):
        super(Server_Show, self).__init__()  # Call the inherited classes __init__ method
        uic.loadUi('ScreenServer_Main.ui', self)  # Load the .ui file
        # self.pushButtonCloseServer.clicked.connect(self.gotoCloseServer)
        self.plainTextEdit.setPlainText(datatext)


app = QtWidgets.QApplication(sys.argv)
window = Server_Main()
widget = QtWidgets.QStackedWidget()
widget.addWidget(window)

widget.setFixedWidth(1000)
widget.setFixedHeight(750)
widget.show()
app.exec_()