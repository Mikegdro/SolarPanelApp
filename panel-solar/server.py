from Sol import Sol
import socketio
# import cv2
import os
import time

# Clase PanelServer
class PanelServer:

    # Constructor de la clase y declaración de métodos
    def __init__(self):

        self.sio = socketio.Client(logger=True, engineio_logger=True)
        self.panel = None

        # Evento de conexión con el servidor
        @self.sio.event
        def connect():
            print('Connection established')
            print('Initializing Solar Panel')
            self.panel = Sol()

        # Evento de mensaje
        @self.sio.on('solar-panel-photo')
        def message_handler(data):

            print('taking photo')

            img = cv2.imread('./sunLowRes.jpg')

            file = open('./sunLowRes.jpg', "rb")
            file_data = file.read(56000)

            try:
                self.sio.emit('message', {
                    "data": file_data,
                })

            except:
                print("f")

        # Evento de tomar foto
        @self.sio.on("take-photo")
        def take_photo():
            print('taking photo')

            img = cv2.imread('./sunLowRes.jpg')

            file = open('./sunLowRes.jpg', "rb")
            file_data = file.read(56000)

            try:
                self.sio.emit('message', {
                    "data": file_data,
                })

            except:
                print("f")

        # Evento de prueba
        @self.sio.on('test')
        def test():
            #Comando de foto
            os.system('python3 <nombre-archivo>')

            # Leemos la salida de texto del script de la pi
            resultado = open('fiechero de salida aquí')
            status = resultado.readline()

            #Mientras la salida no sea que el programa ha terminado
            while status == '1':
                time.sleep(1)
                status = resultado.readline()  

            #Comando de movimiento
            os.system('python3 <nombre-archivo>')

            #Leemos la salida de texto del script de la pi
            resultado = open('fichero de salida aquí')
            status = resultado.readline()

            #Mientras no sea que el programa ha terminado 
            while status == '1':
                time.sleep(1)
                status = resultado.readline()

            try:
                self.sio.emit('comando acabado')
            except:
                print('comando ejecutado')

        # Evento de desconexión
        @self.sio.event
        def disconnect():
            print('disconnected from server')
    
    # Función que recibe la ip del servidor principal e intenta conectarse 
    def connect(self, ip):
        #Para que la conexión funcione se tiene que conectar a un nombre de espacios concreto
        self.sio.connect(ip, wait_timeout = 10, auth={
            'token': 'holi'
        })
        
        self.sio.wait()

# Creación de la clase e instrucción de conexión con la IP
coms = PanelServer("coms")
coms.connect('http://localhost:3000')


