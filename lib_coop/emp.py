from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes

import json


class MepProtocol:
    def __init__(self,socket):
        self.socket = socket

        self.performed_handshake = False
        self.onHandshakeFinisch_F =None

        self.own_private_key,self.own_public_key=generate_key_pair()

        self.extern_pub_key=self.ask_public_key()
        self.waiting_for_success_handshake = False

        self.encripttoken = None

    def ask_public_key(self):
        pass

    def format_jso(self,head,body):
        r=json.dumps({"head":head,"body":body})
        self.__send_any(r.encode('utf-8'))

    def receive_handshake(self, data):
        j=json.loads(data.decode('utf-8'))
        head=j["head"]
        if head != "~handshake" :
            print("handshake not found")
            self.socket.close()

            return
        body=j["body"]
        if "public_key" not in body:
            print("!<>  handshake not found")
            self.socket.close()

            return
        else:
            self.extern_pub_key=deserialize_key(body["public_key"])
            j={"head":"*handshake","body":{"public_key":serialize_key(self.own_public_key)}}
            self.socket.send(json.dumps(j).encode('utf-8'))
            self.performed_handshake=True
            print(">~handshake")
            return


    def do_handshake(self):
        j={"head":"~handshake","body":{"public_key":serialize_key(self.own_public_key)}}

        self.socket.send(json.dumps(j).encode('utf-8'))
        self.waiting_for_success_handshake=True




    def _is__internal_request(self,jso):
        match jso["head"]:
            case "ama":

                return True
            case _:
                return False


    def receive_jso(self,data):
        data=json.loads(data)
        head=data["head"]
        body=data["body"]
        return head,body

    def recive_sucksesfullhandshake(self,data):
        j=json.loads(data.decode('utf-8'))
        head=j["head"]
        body=j["body"]
        if head != "*handshake":
            print("!<> handshake not found")
            self.socket.close()

            return
        else:
            self.extern_pub_key=deserialize_key(body["public_key"])
            self.waiting_for_success_handshake=False
            self.performed_handshake=True
            print(">*handshake")
            return


    def any(self, data):
        try:
            if not self.performed_handshake:
                print("!A")
                if self.waiting_for_success_handshake:
                    print("!")
                    self.recive_sucksesfullhandshake(data)
                    if self.onHandshakeFinisch_F is not None:
                        self.onHandshakeFinisch_F()
                    return None
                self.receive_handshake(data)
                return None
        except Exception as E:
            print("e",E)
            return None




        try:
            data=decrypt(data,self.own_private_key)
        except Exception as e :
            print("Data Error e:",e)
            return None
        return self.receive_jso(data)


    def send(self,head,body):
        jso={"head":head,"body":body}
        jso=json.dumps(jso)
        jso=encrypt(jso,self.extern_pub_key)

        self.__send_any(jso)


    def __send_any(self,message):
        self.socket.send(message)

def generate_key_pair():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key

def encrypt(message, public_key):
    ciphertext = public_key.encrypt(
        message.encode('utf-8'),
        padding.PKCS1v15()
    )
    return ciphertext

def decrypt(ciphertext, private_key):
    plaintext = private_key.decrypt(
        ciphertext,
        padding.PKCS1v15()
    )
    return plaintext.decode('utf-8')

def serialize_key(key):
    return key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode('utf-8')

def deserialize_key(public_key_str):
    public_key_bytes = public_key_str.encode('utf-8')
    return serialization.load_pem_public_key(public_key_bytes, backend=default_backend())
