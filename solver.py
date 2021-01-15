#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 17:52:06 2021

@author: joseguerra

Solver del cubo rubic utilizando opencv y kociemba

14/01/2021: version 0.0.1 -- Version inicial
14/01/2021: version 0.1.0 -- El algoritmo es capaz de reconocer los 6 colores de cada cara.

"""

import cv2 as cv
import numpy as np


while True:
    cap = cv.VideoCapture(0) #seleccion de la camara que deseo utilizar, normalmente usar 0 busca la camara web
    is_ok, bgr_image_input = cap.read() #adquiero el frame del video
    cv.imshow("test", bgr_image_input) #muestra el video. 
    k = cv.waitKey(1) #k = 1 es para espacio, para interrumpir el proceso.

    if k%256 == 27:
        # ESC presionado para cerrar
        cv.destroyWindow("test")
        cv.waitKey(1)
        print("Escape presionado, cerrando...")
        break
    
    hsv =  cv.cvtColor(bgr_image_input,cv.COLOR_BGR2HSV) #paso de rgb a hsv para detectar los colores


    #mascaras
    #mascara verde
    green = cv.inRange(hsv, (25, 0, 0), (80, 255,255))
    
    #mascara amarilla
    yellow = cv.inRange(hsv, (15,0,0), (36, 255, 255))
    
    #mascara azul
    blue = cv.inRange(hsv, (89,178,51), (120,255,195))
    
    #mascara naranja
    orange = cv.inRange(hsv, (1, 190, 200), (18, 255, 255))
    
    #mascara blanca
    white = cv.inRange(hsv, (0, 0, 200), (147, 65, 255))
    
    #para el rojo se usand dos mascaras
    lower_red = np.array([0,50,50])
    upper_red = np.array([10,255,255])
    mask0 = cv.inRange(hsv, lower_red, upper_red)
    
    # upper mask (170-180)
    lower_red = np.array([170,50,50])
    upper_red = np.array([180,255,255])
    mask1 = cv.inRange(hsv, lower_red, upper_red)
    
    #mascara roja
    red = mask0+mask1
    
    ## final mask and masked
    mask = orange + white + blue + green + red #sumo todas las mascaras para encontrar los 6 colores en la imagen
    target = cv.bitwise_and(bgr_image_input,bgr_image_input, mask=mask) #muestro solo los colores de interes.
    
    cv.imshow("target", target)
    
cv.destroyAllWindows()
cv.waitKey(1)
    