import json
from .encrp import Encrp_class
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
