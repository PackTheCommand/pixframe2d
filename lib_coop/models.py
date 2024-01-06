import socket
import threading
from tkinter import Tk, Button

import emp

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []
        self.emp_inst_dict = {}
        self.connected_uuids= {}

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Server listening on {self.host}:{self.port}")

        while True:
            client_socket, addr = self.server_socket.accept()
            print(f"Accepted connection from {addr}")

            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.start()
            self.clients.append((client_socket, client_thread))

    def handle_client(self, client_socket):
        emp_inst=emp.MepProtocol(client_socket)
        uuid=hash(client_socket.getpeername())
        self.emp_inst_dict[uuid]=emp_inst
        print(f"Handling client {client_socket.getpeername()}")
        while True:
            try:
                data = client_socket.recv(1024)
                if not data:
                    break

                # Call the examine method with the received data
                self.examine(emp_inst,data,uuid)

            except Exception as e:
                print(f"Error: {e}")
                break

        client_socket.close()

    def examine(self,emp_inst, data,uuid):
        r=emp_inst.any(data)
        if r:
            head,body=r

            if head=="message":
                print(f"Received data: {head}, {body}")
                receivers=body["r"]
                sender=body["s"]
                message=body["c"]



                for receiver in receivers:
                    if not receiver in self.connected_uuids:
                        emp_inst.send("err-connection", "User Not Connected")

                    else:
                        try:
                            re=self.emp_inst_dict[self.connected_uuids[receiver]]
                            print(f"Sending message to {receiver}")
                            re.send("message",{"s":sender,"c":message,"uuid":body["uuid"]})
                            emp_inst.send("send_confirm",{"r":receiver})
                        except Exception as e:
                            print(f"Error -: {e}")
                            emp_inst.send("err-connection","User Not Connected")
                            self.emp_inst_dict.pop(self.connected_uuids[receiver])
                            self.connected_uuids.pop(receiver)


            elif head=="i-am":
                username=body["username"]
                self.connected_uuids[username]=uuid







class Client:
    def __init__(self, host, port,username):
        self.host = host
        self.port = port
        self.username = username
        self.receveFunction=lambda head,body:print(f"Received data: {head}, {body}")

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.emp_inst = emp.MepProtocol(self.client_socket)


    def connect(self):
        self.client_socket.connect((self.host, self.port))
        print(f"Connected to server on {self.host}:{self.port}")


        self.emp_inst.onHandshakeFinisch_F=lambda u=self.username:self.Iam(u)
        self.emp_inst.do_handshake()


        self.listen_for_data()

    def send_data(self,type, data):
        self.emp_inst.send(type,data)

    def close(self):
        self.client_socket.close()

    def Iam(self,username):
        self.send_data("i-am",{"username":username})

    def listen_for_data(self):

        emp_inst=self.emp_inst
        while True:
            try:
                data = self.client_socket.recv(1024)
                if not data:
                    break

                # Process the received data as needed
                self.process_received_data(emp_inst,data)

            except IOError as e:
                print(f"Error: {e}",data)
                break

    def process_received_data(self,emp_inst, data):

        r=emp_inst.any(data)
        if r:
            head,body=r
            self.receveFunction(head,body)


def beHost():
    server = Server("localhost", 5555)
    server_thread = threading.Thread(target=server.start)
    server_thread.start()

    """client1 = Client("localhost", 5555)
    #client2 = Client("localhost", 5555)

    client_thread1 = threading.Thread(target=client1.connect)
    #client_thread2 = threading.Thread(target=client2.connect)

    client_thread1.start()
    #client_thread2.start()

    #

    # Wait for threads to finish

    #client_thread2.join()


    tk=Tk()

    def sendMessage():
        client1.send_data("message","You are connected ! ")
        return

    b=Button(tk,text="Send",command=lambda:sendMessage())
    b.pack()
    tk.mainloop()"""