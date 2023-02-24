from Sol import Sol
import socketio
import base64
import cv2
import sys
import magic

class Communication:

    def __init__(self, name):

        self.name = name

        self.sio = socketio.Client(logger=True, engineio_logger=True)

        #Inicio de la aplicación
        @self.sio.event
        def connect():
            print('connection established')
            # self.sio.emit('solar-panel-update', {
            #     'panelId': '1234'
            # })

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

        @self.sio.event
        def disconnect():
            print('disconnected from server')
    
    def connect(self, ip):
        #Para que la conexión funcione se tiene que conectar a un nombre de espacios concreto
        self.sio.connect(ip, wait_timeout = 10, auth={
            'token': 'holi'
        })
        self.sio.wait()

coms = Communication("coms")
coms.connect('http://localhost:8023')


