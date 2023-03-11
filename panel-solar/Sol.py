import cv2
import numpy as np
import time

class Sol:

    # Esta función ejecuta el comando de sistema que hace que el panel solar haga una foto al sol
    def takePhoto( self ):
        #Por ahora coge una foto de local
        try:
            self.img = cv2.imread("./sunLowRes.jpg", cv2.IMREAD_COLOR)
            print("Imagen Abierta")
        except IOError:
            print("Error"+IOError)

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

            return {ejex, ejey}
    
    # Devuelve la foto almacenada en la clase
    def getPhoto( self ):
        return self.img

    # Constructor de la clase
    def __init__( self ):
        self.auto = True
        self.img = None
        self.coords = None

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

    # Función que ejecuta el algoritmo de cálculo y ejecuta
    # los comandos del sistema para mover la placa
    def movePanel( self ):
        print('Moviendo Panel')
        
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

sol = Sol()