import json
from datetime import datetime

# Idioma "es-ES" (código para el español de España)
#locale.setlocale(locale.LC_ALL, 'es_pe')
#print(locale.locale_alias)

class Schedule():
    def __init__(self, cur_dir):
        self.cur_dir = cur_dir
        self.cursos = None
        self.current = None
        self.is_active = False
        self.json_file = self.cur_dir + '/info/horario_de_hoy.txt'
        self.now = datetime.now()

    def set_cursos(self, cursos):
        self.cursos = cursos
        self.current = 0
        self.json_update()
        self.obtener_curso_actual()
        
    def get_cursos(self):
        return self.cursos

    def iniciar_curso(self):
        curso = self.cursos[self.current]
        print("\n *** Siguiente curso")
        print(" {0}".format(curso['curso']))
        print(" {0}".format(curso['hora']))
        print(" {0}".format(curso['meet']))
        print(" ***\n")
        return curso['meet']

    def obtener_curso_actual(self):
        if(len(self.cursos) > 0):
            self.current = 0
            hora_ini = self.cursos[self.current]['hora'].split(' ')[1]
            hora_act = self.now.strftime('%H')
            
            while(self.hay_cursos() and Schedule.get_number(hora_ini) < int(hora_act)):
                hora_ini = self.cursos[self.current]['hora'].split(' ')[1]
                self.current += 1
            self.current -= 1
            
            hora_fin = self.cursos[self.current]['hora'].split(' ')[3]
            if(Schedule.get_number(hora_fin) > int(hora_act) and Schedule.get_number(hora_ini) <= int(hora_act)):
                self.is_active = True
    #        elif(Schedule.get_number(hora_fin) < int(hora_act)):
    #            self.is_active = False
            else:
                self.is_active = False
                if(Schedule.get_number(hora_fin) <= int(hora_act)):
                    self.current += 1
        
        
    def imprimir_horario(self):
        print("\n  --- Inicio Horarios --- \n")
        i = 0
        for sched in self.cursos:
            if(i == self.current):
                print("            ***       ****      ***")
                print("            *** Siguiente curso ***")
                print("            ***       ****      ***")
            print(" Hora: {0}".format(sched['curso']))
            print(" Curso: {0}".format(sched['hora']))
            print(" Fecha: {0}".format(sched['fecha']))
            print(" Google meet: {0}\n".format(sched['meet']))
            i += 1
        print("  ---  Fin Horarios  --- \n")

    def hay_cursos(self):
        return True if self.current < len(self.cursos) else False

    def json_listo(self):
        try: 
            with open(self.json_file) as f:
                self.cursos = json.load(f)
                if(self.cursos == []):
                    return True
                
                actual_day = self.now.strftime('%d %B %Y')
                json_day = self.cursos[0]['fecha']
                if(Schedule.compara_fechas(actual_day, json_day)):
                    print(" {0} listo\n".format(self.json_file))
                    # obtener curso actual
                    self.obtener_curso_actual()
                    return True
                else:
                    print(" {0} desactualizado {1} != {2}\n".format(self.json_file, self.now.strftime('%d %B %y'), json_day))
                    return False
        except FileNotFoundError:
            print(" {0} no existe\n".format(self.json_file))
            return False

    def json_update(self):
        with open(self.json_file, 'w') as outfile:
            json.dump(self.cursos, outfile)

    def tiempo_libre(self):
        hora_ini = Schedule.get_number(self.cursos[self.current]['hora'].split(' ')[1])
        hora_act = int(self.now.strftime('%H'))
        min_act = int(self.now.strftime('%M'))
        minutos_act = hora_act*60 + min_act
        return str(hora_ini*60 - minutos_act)

    def tiempo_restante(self):
        hora_fin = Schedule.get_number(self.cursos[self.current]['hora'].split(' ')[3])
        hora_act = int(self.now.strftime('%H'))
        min_act = int(self.now.strftime('%M'))
        minutos_act = hora_act*60 + min_act
        return str(hora_fin*60 - minutos_act)

    # static func
    def compara_fechas(fecha1, fecha2):
        f1 = fecha1.split(' ')
        f2 = fecha2.split(' ')
        if(int(f1[0]) == int(f2[0])):
            #if(f1[1] == f2[1]):
                #if(f1[2] == f2[2]):
            return True
        return False


    def get_number(strng):
        num = ''
        for c in strng:
            if c.isnumeric():
                num += c
        n = 0
        if(strng[len(strng)-2]) == 'p':
            n = 12
        return int(num) + n