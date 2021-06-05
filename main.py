import os
import sys
from time import sleep
from datetime import datetime
from myclasses.urlleader import UrlLeader
from myclasses.schedule import Schedule
from myclasses.user import Usuario, Encrp_class
from myclasses.encrp import Encrp_class

class Classes_Unsaac():
    def __init__(self):
        self.calendar_url = 'https://calendar.google.com/calendar/'
        self.meet_url = ''
        self.account = Usuario()
        self.classes = UrlLeader()
        self.my_schedule = Schedule()
        self.now = datetime.now()
        self.iniciar()
        #self.procesar_clases()
        self.finalizar()

    def iniciar(self):
        self.limpiar_terminal()
        # Verificar si horario está actualizado
        if(not self.my_schedule.json_listo()):
            # obtener horarios
            # Ingresar calendario
            self.classes.open_browser()
            self.classes.open_url(self.calendar_url)
            if(not self.login()):
                return 0

            print(" Calendario abierto correctamente")
            sleep(3)

            # obtener horarios
            if(not self.obtener_horario()):
                return 0
            
            self.classes.close_browser()
            
        self.limpiar_terminal()
        # imprimir horarios
        self.my_schedule.imprimir_horario()
        if(self.my_schedule.current == None):
            print('Felicidades hoy no tiene cursos')
        else:
            self.procesar_clases()

    def login(self):
        actual_usuario = self.account.obtener_usuario()
        # identificar gmail input
        search = '//input[@id="identifierId"]'
        self.element_found(search)
        # ingrsar gmail
        self.classes.element.send_keys(actual_usuario[0])

        # click button siguiente
        search = '//button[@jsname="LgbsSe"]'
        not self.element_found(search)
        self.classes.element.click()

        # esperar actualizacion de pagina
        sleep(3)

        # ingresar contraseña
        search = '//input[@type="password"]'
        self.element_found(search)
        sleep(1)
        contraseña = Encrp_class.desencriptar(actual_usuario[1], actual_usuario[2])
        self.classes.element.send_keys(contraseña)
        
        # click button siguiente
        search = '//button[@jsname="LgbsSe"]'
        self.element_found(search)
        self.classes.element.click()
        print(" Login exitoso")
        return True

    def obtener_horario(self):
        # obtener elementos del dia actual
        search = '//div[contains(@class,"F262Ye") and contains(@class,"YvjgZe")]'
        self.element_found(search)
        
        # obtener horarios, cursos (div)
        search = './/div[@data-dragsource-type="2"]'
        elements = self.classes.find_childs_by_xpath(search)
        cursos = []
        for elem in elements:
            # obtener info de cada curso
            info = str(elem.find_element_by_xpath('.//div[@class="ynRLnc"]').get_attribute('innerHTML')).split(', ')
            info_hora = info[0]
            info_curso = info[1]
            info_fecha = info[5]
            elem.click()
            # obtener link meet de cada curso
            meet_link = str(self.classes.element.find_element_by_xpath('//a[contains(@href,"https://meet.google.com/")]').get_attribute('href'))
            # rellenar informacion de curso
            cursos += [{'hora': info_hora, 'curso': info_curso, 'fecha': info_fecha, 'meet': meet_link.split('?')[0]}]
        self.my_schedule.set_cursos(cursos)

        print(" Horarios obtenidos correctamente")
        return True

    def procesar_clases(self):
        ans = input("Desea abrir la siguiente clase? [Yes/no]: ")
        if(self.my_schedule.hay_cursos() and (ans == 'yes' or ans == 'y' or ans == 'YES' or ans == 'Y' or ans == ' ' or ans == '')):
            # limpiar terminal
            self.limpiar_terminal()
            if(self.my_schedule.is_active):
                print(" El curso está abierto, quedan {0} minutos para finalizar\n".format(self.my_schedule.tiempo_restante()))
            else:
                print(" Falta {0} minutos para iniciar el curso\n".format(self.my_schedule.tiempo_libre()))

            self.meet_url = self.my_schedule.iniciar_curso()
            self.abrir_clase()
        
        if(not self.my_schedule.hay_cursos()):
            print("\n Felicidades, ya no tiene más cursos\n")
    
    def abrir_clase(self):
        self.classes.open_browser()
        self.classes.open_url(self.calendar_url)
        self.login()
        self.classes.new_window()
        sleep(3)
        self.classes.open_url(self.meet_url)
        self.entrar_a_clase()
        print(" Ingreso a clase exitoso :)")
    def entrar_a_clase(self):
        # obtener elementos del dia actual
        search = '//div[@class="EhAUAc"]'
        self.element_found(search)
        
        # obtener horarios, cursos (div)
        search = './/div[@role="button"]'
        elements = self.classes.find_childs_by_xpath(search)
        for elem in elements:
            elem.click()
        search = './/div[@jsname="Qx7uuf"]'
        self.element_found(search)
        self.classes.element.click()
        

    def element_found(self, search):
        self.classes.element = None
        self.classes.find_element_by_xpath(search)

    def finalizar(self):
        print(" Adios...\n")

    def limpiar_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        # Saludo
        print(" Utilize 'python3 main.py nuevo' para cambiar de usuario!")
        print("\n Hola {}".format(self.account.obtener_usuario()[0]))
        print(" Hoy es: ", self.now.strftime("%d %B %Y  %H:%M:%S"))

        
if __name__ == "__main__":
    if(len(sys.argv) == 2 and sys.argv[1] == 'nuevo'):
        try: 
            os.remove('user.txt')
            os.remove('horario_de_hoy.txt')
            print("Cambiando usuario")
        except FileNotFoundError:
            print("Nuevo Usuario")

    try: 
        open('user.txt')
    except FileNotFoundError:
        print("Error no existe usuario!")
        try: 
            os.remove('horario_de_hoy.txt')
        except FileNotFoundError:
            print("Error no existen horarios!")
        
    mis_horario_de_hoy = Classes_Unsaac()
