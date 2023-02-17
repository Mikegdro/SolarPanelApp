import socketio

class Communication:

    def __init__(self, name):

        self.name = name

        self.sio = socketio.Client(logger=True, engineio_logger=True)

        #Inicio de la aplicación
        @self.sio.event
        def connect():
            print('connection established')
            self.sio.emit('login', {'token': 'token'})

        @self.sio.event
        def my_message(data):
            print(data)

        @self.sio.event
        def disconnect():
            print('disconnected from server')
    
    def connect(self, ip):
        #Para que la conexión funcione se tiene que conectar a un nombre de espacios concreto
        self.sio.connect(ip, namespaces="/panel-solar" ,wait_timeout = 10, socketio_path='/regex')
        self.sio.wait()

coms = Communication("coms")
coms.connect('http://localhost:8023')