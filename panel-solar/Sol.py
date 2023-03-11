import cv2
import numpy as np
import time
import os
import math

class Sol:

    # Esta función ejecuta el comando de sistema que hace que el panel solar haga una foto al sol
    def takePhoto( self ):
        try:
            # # Comando de sistema que hace una foto
            # os.system('python3 <nombre-archivo>')

            # # Leemos la salida de texto de la PI
            # resultado = open('fiechero de salida aquí')
            # status = resultado.readline()

            # # Mientras la salida no sea positiva esperamos
            # while status != '1':
            #     time.sleep(5)
            #     status = resultado.readline()

            #Recogemos la foto realizada
            self.img = cv2.imread("./sunPhoto.jpg", cv2.IMREAD_COLOR)

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

            cv2.imwrite('./result.jpg', self.img)
            
            circles = np.round(detected_circles[0, :]).astype("int")

            ejex = circles[0][0]
            ejey = circles[0][1]
            ejez = circles[0][2]

            return {ejex, ejey, ejez}
    
    # Devuelve la foto almacenada en la clase
    def getPhoto( self ):
        return self.img

    # Constructor de la clase
    def __init__( self, sendInfo ):
        self.auto = True
        self.img = None
        self.coords = None
        self.debug = True

        # Callback con la función a ejecutar para mandar datos
        self.sendInfo = sendInfo

        self.adjustPanel()

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

        #self.sendInfo([self.coords, self.img])

    # Función que ejecuta el algoritmo de cálculo y ejecuta
    # los comandos del sistema para mover la placa
    def movePanel( self ):
        # Info
        print('Moviendo Panel')

        imgCoords = self.img.shape
        self.coords = list(self.coords)
        diffX = imgCoords[1] / 2 - (self.coords[0])
        diffY = imgCoords[0] / 2 - (self.coords[1])

        # Con la hipotenusa podemos comprobar si el centro de la imagen está dentro del radio
        # del sol por lo que podemos optimizar mucho más el programa
        hipotenusa = math.sqrt(pow(diffX, 2) + pow(diffY, 2))

        if self.debug:
            self.debugPanel(imgCoords, diffX, diffY, hipotenusa)

        # Solo movemos las placa cuando el sol no esté en el centro de la foto
        if hipotenusa < self.coords[2]:
            self.moveXAxis(diffX, True)
            self.moveYAxis(diffY, True)
                
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


    def debugPanel( self, imgCoords, diffX, diffY, hipotenusa):
        print("Panel Info:")
        print(' EjeX de la foto:' + str(imgCoords[1] / 2) + ' - ' + 'EjeX de la IA ' + str(self.coords[0]) + ' =  Resultado : ' + str(diffX) + 'px')
        print(' EjeY de la foto:' + str(imgCoords[0] / 2) + ' - ' + 'EjeY de la IA ' + str(self.coords[1]) + ' =  Resultado : ' + str(diffX) + 'px')
        print(' Datos de la Imagen ' + str(imgCoords), 'Datos devueltos de la IA ' + str(self.coords))
        print(' Distancia del centro de la foto al centro del sol: ' + str(hipotenusa) + ' px')
        
        if hipotenusa < self.coords[2]:
            print(' El sol está en el centro de la foto')
        else:
            print(' El sol no está en el centro de la foto')

    # Mueve la placa en el EjeX        
    def moveXAxis( self, amount, auto ):
        
        # Alteramos la variable auto con la que nos entra
        # será True si es interna, False si es externa (comando usuario)
        self.auto = auto

        # Comando de movimiento
        os.system('python3 <nombre-archivo> xAxis' + str(amount))

        # Esperamos 5 segundos y comprobamos si ha terminado
        time.wait(5)


    # Mueve la placa en el EjeY
    def moveYAxis( self, amount, auto):
        # Alteramos la variable auto con la que nos entra
        # será True si es interna, False si es externa (comando usuario)
        self.auto = auto

        #Comando de movimiento
        os.system('python3 <nombre-archivo> yxAxis' + str(amount))

def sendInfo( info ):
    print('Sending Info', info)

sol = Sol(sendInfo)