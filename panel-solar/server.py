from Sol import Sol
import socketio
import base64
import cv2
import sys

class Communication:

    def __init__(self, name):

        self.name = name

        self.sio = socketio.Client(logger=True, engineio_logger=True)

        #Inicio de la aplicación
        @self.sio.event
        def connect():
            print('connection established')
            self.sio.emit('solar-panel-update', {
                'panelId': '1234'
            })

        @self.sio.on('solar-panel-photo')
        def message_handler(data):

            print('solar')
            # sol = Sol
            # sol.findCircle(sol)
            # img = sol.getPhoto(sol)

            img = cv2.imread('./sun.png')
            # img = cv2.imencode('.jpg', img)
            # encoded_string = base64.b64encode(img);

            # self.sio.emit('solar-panel-photo', {

            # })

            print(sys.getsizeof(img) * 1* 10 ** -3)

            
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
coms.connect('http://192.168.108.4:3000')


