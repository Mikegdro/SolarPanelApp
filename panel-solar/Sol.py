from PIL import Image
import cv2
import numpy as np

class Sol:

    def __init__(self, name):
        self.name = name

    # def takePhoto(self):
    #     #Por ahora coge una foto de local
    #     try:
    #         self.img = cv2.imread("./sunLowRes.jpg", cv2.IMREAD_COLOR)
    #         print("Imagen Abierta")
    #     except IOError:
    #         print("Error"+IOError)

    def findCircle(self):

        #Imagen
        self.img = cv2.imread("./sunLowRes.jpg", cv2.IMREAD_COLOR)

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

            cv2.imwrite('./test.jpg', self.img)
    
    def getPhoto(self):
        return self.img

    

sol = Sol("hi")
sol.takePhoto()
sol.findCircle()