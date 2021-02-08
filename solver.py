#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 17:52:06 2021
@author: joseguerra
Solver del cubo rubic utilizando opencv y kociemba
14/01/2021: version 0.0.1 -- Version inicial
14/01/2021: version 0.1.0 -- El algoritmo es capaz de reconocer los 6 colores de cada cara.
08/02/2021: version 0.2.0 -- Mejoras al reconocimiento de cada cara. De momento detecta los 6 stickers por cara
                             falta deteccion de color. Ruido eliminado, el 90% de las veces se enfoca unicamente 
                             en los 6 stickers. 
"""

import cv2 as cv
import numpy as np

# cap = cv.VideoCapture(0) #seleccion de la camara que deseo utilizar, normalmente usar 0 busca la camara web
# cap.set(cv.CAP_PROP_FRAME_WIDTH, 130) 
# cap.set(cv.CAP_PROP_FRAME_HEIGHT,130)

kernel = np.ones((5,5), np.uint8) 
#font = cv.FONT_HERSHEY_COMPLEX

class Rubiks():
     def __init__(self,cam_num = 0, WIDTH = 120, HEIGHT = 120):
        self.cap = cv.VideoCapture(cam_num)
        self.cap.set(cv.CAP_PROP_FRAME_WIDTH, WIDTH)
        self.cap.set(cv.CAP_PROP_FRAME_HEIGHT, HEIGHT)
        self.cam_num = cam_num
    
     def Get_squares(self):
        
        while True:
            is_ok, image = self.cap.read() #adquiero el frame del video
            cv.imshow("test", image) #muestra el video. 
            k = cv.waitKey(1) #k = 1 es para espacio, para interrumpir el proceso.
            gray_image = cv.cvtColor(image, cv.COLOR_BGR2HSV) #paso 1, pasar a blanco y negro
            
            blur_image = cv.GaussianBlur(gray_image, (11, 11), 0) #difuminado, para quitar detalles extras, paso 2
            edge = cv.Canny(blur_image, 150, 250,3) #Con canny busca los bordes, paso 3
            img_dilation = cv.dilate(edge, kernel, iterations=1) #dilatacion, paso 4
            cv.imshow("dilatacion", img_dilation) #muestra la imagen
            
            r, t = cv.threshold(img_dilation, 200, 265, cv.THRESH_BINARY_INV)
            _,cnts,h = cv.findContours(t, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)
            cnts = sorted(cnts, key=cv.contourArea, reverse=True)
            #cv.drawContours(image, cnts, -1, (0,0,255), thickness = 5)
            contour_list = [] #array que guarda los contornos circulares encontrados
            for con in cnts:
                approx = cv.approxPolyDP(con, 0.1*cv.arcLength(con, True), True) 
                if (len(approx) == 4):
                    x,y,w,h = cv.boundingRect(con)
                    area = cv.contourArea(con)#Rectangle area
                    print(area)
                    if w<25 and w > 15 and h<25 and h > 15 and area > 230:
                        cv.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)
                        contour_list.append(con)
                        
            cv.imshow("contornos", image)
        
            if k%256 == 27:
                # ESC presionado para cerrar
                cv.destroyWindow("test")
                cv.waitKey(1)
                print("Escape presionado, cerrando...")
                break
            
        cv.destroyAllWindows()
        cv.waitKey(1)

