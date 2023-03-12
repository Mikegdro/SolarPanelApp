from Sol import Sol
import socketio

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

        # Evento de activación/desactivación del modo auto del panel
        @self.sio.on('solar-panel-auto')
        def switchAuto():
            self.panel.switchAuto()

        # Evento de mover panel
        @self.sio.on("solar-panel-move")
        def movePanel(data):
            self.panel.moveAxis(data[0], data[1], False)

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


