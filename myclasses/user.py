import json
import random

class Usuario():
    def __init__(self):
        self.__user = []
        self.logged = False
        self.json_file = 'user.txt'
        self.json_init()
    def json_init(self):
        try: 
            with open(self.json_file) as f:
                self.__user = json.load(f)
        except FileNotFoundError:
            self.login_user()
    def login_user(self):
            print("*** Login ***")
            username = input("Ingrese email: ")
            password = input("Ingrese password: ")
            password_enc = Encrp_class.encriptar(password)
            self.__user = [username, password_enc[1], password_enc[0]]
            self.crear_json()
    def crear_json(self):
        with open(self.json_file, 'w') as outfile:
            json.dump(self.__user, outfile)
    def update_usuario(self):
        self.login_user()
    def obtener_usuario(self):
        user = [self.__user[0], self.__user[1], self.__user[2]]
        return user

class Encrp_class():
    def encriptar(strng):
        llave = ''
        strng_enc = ''
        for c in strng:
            num = random.randint(1,26)
            llave = chr(num) + llave
            strng_enc += chr(ord(c) + num)
        return [strng_enc,llave]

    def desencriptar(llave, strng_enc):
        strng = ''
        l = len(llave)
        for c in strng_enc:
            num = ord(llave[l - 1])
            strng += chr(ord(c) - num)
            l -= 1
        return strng
