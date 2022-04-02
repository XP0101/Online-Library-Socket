import sys
import socket
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.QtWidgets import QMessageBox

import select
import errno
checkView = False
HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = 54005
screenCURR = 2


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

class Client_Login(QtWidgets.QMainWindow):
    def __init__(self):
        super(Client_Login, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('ScreenClient_LOGIN.ui', self) # Load the .ui file
        self.lineEditPASS.setEchoMode(QtWidgets.QLineEdit.Password)

        self.pushButtonLOGIN.clicked.connect(self.gotoScreenHOME)
        self.pushButtonCREATEACC.clicked.connect(self.gotoScreenSIGNUP)

    def gotoScreenHOME(self):
        global client_socket
        username = self.lineEditUSER.text().encode('utf-8')
        username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
        client_socket.send(username_header + username)

        password = self.lineEditPASS.text().encode('utf-8')
        password_header = f"{len(password):<{HEADER_LENGTH}}".encode('utf-8')
        client_socket.send(password_header + password)

        self.lineEditUSER.setText('')
        self.lineEditPASS.setText('')


        check = '0'.encode('utf-8')
        check_header = f"{len(check):<{HEADER_LENGTH}}".encode('utf-8')
        client_socket.send(check_header + check)
        global screenCURR

        try:
            while True:
                message_header = client_socket.recv(HEADER_LENGTH)
                if not len(message_header):
                    print('Connection closed by the server')
                    sys.exit()
                message_length = int(message_header.decode('utf-8').strip())
                message = client_socket.recv(message_length).decode('utf-8')


                if message == "1":
                    widget.setCurrentIndex(2)
                    break
                else:
                    msg = QMessageBox()
                    msg.setText('Connection failed!')
                    x = msg.exec_()
                    client_socket.close()
                    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    client_socket.connect((IP, PORT))

                    widget.setCurrentIndex(0)

                    break
        except :
            sys.exit()


    def gotoScreenSIGNUP(self):
        widget.setCurrentIndex(1)



class Client_HOME(QtWidgets.QMainWindow):
    def __init__(self):
        super(Client_HOME, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('ScreenClient_HOME.ui', self) # Load the .ui file
        self.pushButtonLOGOUT.clicked.connect(self.gotoScreenLOGIN)
        self.pushButtonSEARCH.clicked.connect(self.gotoScreenINFOR_BOOK)

    def gotoScreenLOGIN(self):
        global client_socket
        client_socket.close()
        widget.setCurrentIndex(0)
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((IP, PORT))


    def gotoScreenINFOR_BOOK(self):
        mess = self.lineEditSEARCH.text()
        self.lineEditSEARCH.setText('')
        check = False
        global screenCURR
        if ('F_ID' in mess or 'F_Name ' in mess or 'F_Type ' in mess or 'F_Author ' in mess ):

            mess1 = mess.encode('utf-8')
            mess_header = f"{len(mess1):<{HEADER_LENGTH}}".encode('utf-8')
            client_socket.send(mess_header + mess1)
            check = True
        if(check == False):
            msg = QMessageBox()
            msg.setText('Syntax error!')
            x = msg.exec_()

            widget.setCurrentIndex(2)

        else:
            screen = Client_INFOR_BOOK()
            widget.addWidget(screen)
            screenCURR += 1

            widget.setCurrentIndex(screenCURR)




class Client_SIGNUP(QtWidgets.QMainWindow):
    def __init__(self):
        super(Client_SIGNUP, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('ScreenClient_SIGNUP.ui', self) # Load the .ui file
        self.lineEditPASS.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEditPASSCONFIRM.setEchoMode(QtWidgets.QLineEdit.Password)
        self.pushButtonCONFIRM.clicked.connect(self.gotoScreenLOGIN)

    def gotoScreenLOGIN(self):
        global client_socket
        user = self.lineEditUSER.text()
        self.lineEditUSER.setText('')
        password = self.lineEditPASS.text()
        self.lineEditPASS.setText('')
        confirmpass = self.lineEditPASSCONFIRM.text()
        self.lineEditPASSCONFIRM.setText('')
        if (password!= confirmpass):
            msg = QMessageBox()
            msg.setText('Registration failed!')
            x = msg.exec_()
        else:
            user = user.encode('utf-8')
            user_header = f"{len(user):<{HEADER_LENGTH}}".encode('utf-8')
            client_socket.send(user_header + user)

            password = password.encode('utf-8')
            pass_header = f"{len(password):<{HEADER_LENGTH}}".encode('utf-8')
            client_socket.send(pass_header + password)

            check = "SIGNUP".encode('utf-8')
            check_header = f"{len(check):<{HEADER_LENGTH}}".encode('utf-8')
            client_socket.send(check_header+check)

            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode('utf-8').strip())
            message = client_socket.recv(message_length).decode('utf-8')

            if message == "1":
                client_socket.close()
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.connect((IP, PORT))
                widget.setCurrentIndex(0)
            else:
                msg = QMessageBox()
                msg.setText('Unsuccessfully SignUp!')
                x = msg.exec_()

                widget.setCurrentIndex(1)

class Client_INFOR_BOOK(QtWidgets.QMainWindow):
    def __init__(self):
        super(Client_INFOR_BOOK, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('ScreenClient_INFOR_BOOK.ui', self) # Load the .ui file
        self.tableWidgetINFOR.setColumnWidth(0,100)
        self.tableWidgetINFOR.setColumnWidth(1, 389)
        self.tableWidgetINFOR.setColumnWidth(2, 200)
        self.tableWidgetINFOR.setColumnWidth(3, 200)
        self.loadData()
        self.pushButtonBACK.clicked.connect(self.gotoScreenHOME)
        self.pushButtonVIEW.clicked.connect(self.gotoScreenVIEW)
        self.pushButtonDOWNLOAD.clicked.connect(self.gotoScreenDOWNLOAD)

    def loadData(self): # Nhận dữ liệu từ server và xuất ra màn hình
        data = ""
        row = 0
        while True:
            data_header = client_socket.recv(HEADER_LENGTH)
            data_length = int(data_header.decode('utf-8').strip())
            data = client_socket.recv(data_length).decode('utf-8')
            if data == "EXIT":
                return
            infor = data.split(", ") # Tách mỗi dòng trong InforBook.txt thành mảng thông tin
            self.tableWidgetINFOR.setRowCount(10)
            self.tableWidgetINFOR.setItem(row, 0, QtWidgets.QTableWidgetItem(infor[0]))
            self.tableWidgetINFOR.setItem(row, 1, QtWidgets.QTableWidgetItem(infor[1]))
            self.tableWidgetINFOR.setItem(row, 2, QtWidgets.QTableWidgetItem(infor[2]))
            self.tableWidgetINFOR.setItem(row, 3, QtWidgets.QTableWidgetItem(infor[3]))
            row += 1

    def gotoScreenHOME(self):
        widget.setCurrentIndex(2)


    def gotoScreenVIEW(self):
        global screenCURR
        screen = Client_VIEW_BOOK(self.lineEditBOOK_ID.text())
        widget.addWidget(screen)
        screenCURR += 1
        widget.setCurrentIndex(screenCURR)

    def gotoScreenDOWNLOAD(self): # gửi cho server chức năng DOWNLOAD và gửi IDBOOK
        mess_func = 'DOWNLOAD'.encode('utf-8')
        mess_func_header = f"{len(mess_func):<{HEADER_LENGTH}}".encode('utf-8')
        client_socket.send(mess_func_header + mess_func)

        ID_Book = self.lineEditBOOK_ID.text().encode('utf-8')
        IDBook_header = f"{len(ID_Book):<{HEADER_LENGTH}}".encode('utf-8')
        client_socket.send(IDBook_header + ID_Book)

        data_header1 = client_socket.recv(HEADER_LENGTH) # Nhận Exit hoặc tên file sách cần tải (vd:001.txt)
        data_length1 = int(data_header1.decode('utf-8').strip())
        data1 = client_socket.recv(data_length1).decode('utf-8')

        data_header2 = client_socket.recv(HEADER_LENGTH)    # Nhận Exit hoặc nội dung sách
        data_length2 = int(data_header2.decode('utf-8').strip())
        data2 = client_socket.recv(data_length2)

        if data1 == "EXIT":         # nếu Exit thì sách không tồn tại
            msg = QMessageBox()
            msg.setText('Unsuccessfully Download!')
            x = msg.exec_()
        else:
            with open("D:\\"+data1,'wb') as f:      # địa chỉ lưu sách
                f.write(data2)
                msg = QMessageBox()
                msg.setText(f'Download successfully! \n Save at D:\\{data1}')
                x = msg.exec_()
                f.close()
        return


class Client_VIEW_BOOK(QtWidgets.QMainWindow):
    def __init__(self,ID_Book):
        super(Client_VIEW_BOOK, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('ScreenClient_VIEWBOOK.ui', self) # Load the .ui file
        mess_func = 'VIEW'.encode('utf-8')
        mess_func_header = f"{len(mess_func):<{HEADER_LENGTH}}".encode('utf-8')
        client_socket.send(mess_func_header + mess_func)
        self.showBook(ID_Book)
        self.pushButtonBACK.clicked.connect(self.gotoScreenINFOR_BOOK)


    def showBook(self,ID_Book):
        ID_Book = ID_Book.encode('utf-8')
        IDBook_header = f"{len(ID_Book):<{HEADER_LENGTH}}".encode('utf-8')
        client_socket.send(IDBook_header + ID_Book)

        data_header = client_socket.recv(HEADER_LENGTH)
        data_length = int(data_header.decode('utf-8').strip())
        data = client_socket.recv(data_length).decode('utf-8')

        if data == "EXIT":
            self.plainTextEdit.setPlainText("Book doesn't Exist or file .pdf")
        else:
            self.plainTextEdit.setPlainText(data)

        return
    def gotoScreenINFOR_BOOK(self):
        widget.setCurrentIndex(3)
        #print(widget.currentIndex())


app = QtWidgets.QApplication(sys.argv)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))
widget = QtWidgets.QStackedWidget()

window = Client_Login() #0
widget.addWidget(window)

window = Client_SIGNUP() #1
widget.addWidget(window)

window = Client_HOME() #2
widget.addWidget(window)

widget.setFixedWidth(1000)
widget.setFixedHeight(750)
widget.show()
app.exec_()
