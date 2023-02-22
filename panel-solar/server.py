import socketio

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

        @self.sio.event
        def my_message(data):
            print(data)

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
