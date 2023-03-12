import cv2
import numpy as np
import time
import os
import math

import json

from dotenv import load_dotenv

load_dotenv()

class Sol:

    # Constructor de la clase
    def __init__( self, sendInfo ):
        self.auto = True
        self.img = None

        self.coords = None
        self.id = os.getenv("PANEL_ID")

        # Sensores de potencia
        self.sensor1 = None
        self.sensor2 = None
        self.sensor3 = None
        self.sensor4 = None

        # Grados de inclinación de cada eje
        self.motor1 = None
        self.motor2 = None

        # Estado de la batería y potenciómetro
        self.battery = None
        self.potency = None

        # Modo Debug, se activa en el .env
        self.debug = True if os.getenv("DEBUG_MODE") == 'YES' else False

        # Ejecuta los comandos de sistema 
        self.checkPanelHealth() 

        # Callback con la función a ejecutar para mandar datos
        self.sendInfo = sendInfo

        # Función que ejecuta el bucle principal recursivamente
        self.adjustPanel()

    # Función que lee de un archivo status.txt el estado de todas las variables de la placa
    def checkPanelHealth( self ):
        statusFile = open(os.getenv('STATUS_FILE'))
        self.sensor1 = self.getPanelParams('sensor1')
        self.sensor2 = self.getPanelParams('sensor2')
        self.sensor3 = self.getPanelParams('sensor3')
        self.sensor4 = self.getPanelParams('sensor4')
        self.motor1 = self.getPanelParams('motores')[0]
        self.motor2 = self.getPanelParams('motores')[1]
        self.battery = self.getPanelParams('bateria')
        self.potency = 'Potencia?'
        statusFile.close();
        
    # Esta función ejecuta el comando de sistema que hace que el panel solar haga una foto al sol
    def takePhoto( self ):
        try:
            # Comando de sistema que hace una foto
            os.system(os.getenv('PHOTO_COMMAND'))

            # Recogemos la foto realizada
            # DESCOMENTAR EN EL ENV EL ARCHIVO CORRECTO
            self.img = cv2.imread(os.getenv('ORIGINAL_IMAGE_URI'), cv2.IMREAD_COLOR)

            print("Imagen Abierta")

        except Exception:

            print("Error", Exception)

    # Esta función ejecuta la inteligencia artificial y en caso de que el modo auto esté activado ejecta la función de movimiento
    def findCircle( self ):

        # Convert to grayscale.
        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        
        # Blur using 3 * 3 kernel.
        gray_blurred = cv2.blur(gray, (3, 3))
        
        # Apply Hough transform on the blurred image.
        detected_circles = cv2.HoughCircles(gray_blurred, 
                        cv2.HOUGH_GRADIENT, 1, 200, param1 = 10,
                    param2 = 60, minRadius = 20, maxRadius = 100)

        # Draw circles that are detected.
        if detected_circles is not None:
        
            # Convert the circle parameters a, b and r to integers.
            detected_circles = np.uint16(np.around(detected_circles))
        
            for pt in detected_circles[0, :]:
                a, b, r = pt[0], pt[1], pt[2]
        
                # Draw the circumference of the circle.
                cv2.circle(self.img, (a, b), r, (0, 255, 0), 2)
        
                # Draw a small circle (of radius 1) to show the center.
                cv2.circle(self.img, (a, b), 1, (0, 0, 255), 3)
                #cv2.imshow("Detected Circle", self.img)
                cv2.waitKey(0)

            cv2.imwrite(os.getenv('IA_IMAGE_URI'), self.img)
            
            circles = np.round(detected_circles[0, :]).astype("int")

            ejex = int(circles[0][0])
            ejey = int(circles[0][1])
            radio = int(circles[0][2])

            return { ejex, ejey, radio }

    # Función principal llamada de manera recursiva que 
    # establece el loop del programa
    def adjustPanel( self ):
        # Hacemos la foto
        self.takePhoto()

        # Si no tenemos la foto hibernamos
        if self.img is None:
            self.sleep()

        # Si tenemos la foto ejecutamos la IA
        self.coords = self.findCircle()

        # Si la IA no encuentra nada hibernamos
        if self.coords is None:
            self.sleep()

        # Si la IA encuentra algo movemos el panel
        self.movePanel()

        self.updateData( "update" )

        self.sleep()

    # Envía al servidor una actualización con los datos recogidos en el barrido actual
    # Type es el tipo de log se creará, si es "update" será un log de información, si es "error" es un log de error
    # Se puede añadir en un futuro un log "command" que se crea por comando de un usuario administrador
    def updateData( self, type ):
        # Declaramos las variables a null
        image = None
        ocvOutput = None

        # Si ha habido algun error mandámos también las fotos
        if type ==  "error": 
            image1 = open("images/ia.jpg", "rb")
            image = image1.read(56000)
            image1.close()

            image2 = open("images/original.jpg", "rb")
            ocvOutput = image2.read(56000)
            image2.close()

        self.sendInfo({
            "id": self.id,
            "time": time.time(),
            "type": type,
            "log": {
                "sensor1": self.sensor1,
                "sensor2": self.sensor2,
                "sensor3": self.sensor3,
                "sensor4": self.sensor4,
                "motor1": self.motor1,
                "motor2": self.motor2,
                "battery": self.battery,
                "potency": self.potency,
                "image": image,
                "ocvOutput": ocvOutput
            }
        })

    # Función que ejecuta el algoritmo de cálculo y ejecuta
    # los comandos del sistema para mover la placa
    def movePanel( self ):
        # Info
        print('Moviendo Panel')

        # Recogemos las dimensiones de la imagen
        imgCoords = self.img.shape

        self.coords = list(self.coords)

        # Calculamos la diferencia de ambos ejex ( en PX )
        # TODO => PASAR ESTO A º
        diffX = (self.coords[0]) - imgCoords[1] / 2 
        diffY = imgCoords[0] / 2 - (self.coords[1])  
        print(imgCoords, self.coords)

        # Con la hipotenusa podemos comprobar si el centro de la imagen está dentro del radio
        # del sol por lo que podemos optimizar mucho más el programa
        hipotenusa = math.sqrt(pow(diffX, 2) + pow(diffY, 2))

        # Debuging del movimiento del panel
        if self.debug:
            self.debugPanel(imgCoords, diffX, diffY, hipotenusa)

        # Solo movemos las placa cuando el sol no esté en el centro de la foto
        if hipotenusa > self.coords[2]:
            # Motor 1 ( EjeX )
            posicionMotor1 = self.getPanelParams('motores')[0]['grados']
            movimientoMotor = posicionMotor1 - diffX if posicionMotor1 > diffX else posicionMotor1 + diffX
            print("Moviendo el ejeX: ", movimientoMotor)
            self.moveAxis('X', movimientoMotor, True)

            # Motor 2 ( EjeY )
            posicionMotor2 = self.getPanelParams('motores')[1]['grados']
            movimientoMotor = posicionMotor2 - diffY if posicionMotor2 > diffY else posicionMotor2 + diffY            
            print("Moviendo el ejeX: ", movimientoMotor)
            self.moveAxis('Y', movimientoMotor, True)
        
    # Función que duerme el programa el tiempo necesario
    # dependiendo de la situación
    def sleep( self ):
        # Dependiendo del modo de la placa duerme un tiempo u otro
        if self.auto:
            time.sleep(100)
        else:
            time.sleep(300)
            self.auto = True

        self.adjustPanel()

    # Función que saca por consola los datos de los cálculos del panel
    def debugPanel( self, imgCoords, diffX, diffY, hipotenusa):
        print("Panel Info:")
        print(' EjeX de la foto:' + str(imgCoords[1] / 2) + ' - ' + 'EjeX de la IA ' + str(self.coords[0]) + ' =  Resultado : ' + str(diffX) + 'px')
        print(' EjeY de la foto:' + str(imgCoords[0] / 2) + ' - ' + 'EjeY de la IA ' + str(self.coords[1]) + ' =  Resultado : ' + str(diffY) + 'px')
        print(' Datos de la Imagen ' + str(imgCoords), 'Datos devueltos de la IA ' + str(self.coords))
        print(' Distancia del centro de la foto al centro del sol: ' + str(hipotenusa) + ' px')
        
        if hipotenusa < self.coords[2]:
            print(' El sol está en el centro de la foto')
        else:
            print(' El sol no está en el centro de la foto')

    # Le entra el parámetro que se pide de la placa
    def getPanelParams( self, param ):
        # Ejecutamos el archivo estado para generar el archivo con las variables
        os.system(os.getenv('CHECK_STATUS'))

        # Recogemos la salida del comando
        file = open(os.getenv('STATUS_FILE'))
        file = file.read()
        file = json.loads(file)

        return file[param]

    # Mueve la placa en el EjeX        
    def moveAxis( self, axis, amount, auto ):
        
        # Alteramos la variable auto con la que nos entra
        # será True si es interna, False si es externa (comando usuario)
        self.auto = auto

        # Comando de movimiento
        command = os.getenv('MOVE_COMMAND')
        command = command + '1' if axis == 'X' else command + '2'
        command += ' ' + str(amount)
        print("Ejecutando = " + command)

        # Ejecutamos el comando
        os.system(command)
        motor = 0 if axis == 'X' else 1

        # He intentado simular un do while pero esto me chirría muchisimo, aun así me parece más limpio
        # Este bucle se ejecuta como máximo 5 veces, en intervalos de 5 segundos para comprobar si el comando se ha ejecutado apropiadamente
        tries = 0
        while True:
            status = self.getPanelParams('motores')
            finished = not status[motor]['activo']

            if finished or tries >= 5:
                break
            else:
                tries += 1
                time.sleep(5)
            
    # Apaga/enciende el modo automático del panel
    def switchAuto( self ):
        self.auto = not self.auto

# def sendinfo(info):
#     print("Sending info", info)

# sol = Sol(sendinfo)