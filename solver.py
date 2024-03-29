#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 17:52:06 2021
@author: joseguerra
Solver del cubo rubic utilizando opencv y kociemba
14/01/2021: version 0.0.1 -- Version inicial
14/01/2021: version 0.1.0 -- El algoritmo es capaz de reconocer los 6 colores de cada cara. (version eliminada)
08/02/2021: version 0.2.0 -- Mejoras al reconocimiento de cada cara. De momento detecta los 6 stickers por cara
                             falta deteccion de color. Ruido eliminado, el 90% de las veces se enfoca unicamente 
                             en los 6 stickers. 
08/02/2021: version 0.2.1 -- Se implementa una version POO para mejor uso de estas funciones.
27/01/2022: version 0.3.0 -- Nueva funcion para detectar los colores, de momento detecta rojo, azul y amarillo.
27/01/2022: version 0.3.1 -- Recorte de imagen para centrarse en una ROI y detectar unicamente los cuadros del cubo.
                             No hay cambios en los colores que detecta. 
"""

import cv2 as cv
import numpy as np

# cap = cv.VideoCapture(0) #seleccion de la camara que deseo utilizar, normalmente usar 0 busca la camara web
# cap.set(cv.CAP_PROP_FRAME_WIDTH, 130) 
# cap.set(cv.CAP_PROP_FRAME_HEIGHT,130)

kernel = np.ones((5,5), np.uint8) 
font = cv.FONT_HERSHEY_COMPLEX

#-------- para la deteccion de colores
azulBajo = np.array([100,100,20],np.uint8)
azulAlto = np.array([125,255,255],np.uint8)
amarilloBajo = np.array([28,100,20],np.uint8)
amarilloAlto = np.array([33,255,255],np.uint8)
redBajo1 = np.array([0,100,20],np.uint8)
redAlto1 = np.array([5,255,255],np.uint8)

#redBajo2 = np.array([175,100,20],np.uint8)
#redAlto2 = np.array([179,255,255],np.uint8)

class Rubiks():
     def __init__(self,cam_num = 0, WIDTH = 120, HEIGHT = 120):
        self.cap = cv.VideoCapture(cam_num)
        self.cap.set(cv.CAP_PROP_FRAME_WIDTH, WIDTH)
        self.cap.set(cv.CAP_PROP_FRAME_HEIGHT, HEIGHT)
        self.cam_num = cam_num
        #self.image = 0
    
     def Draw_squares_old_version(self):
        
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
            cnts,h = cv.findContours(t, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)
            cnts = sorted(cnts, key=cv.contourArea, reverse=True)
            #cv.drawContours(image, cnts, -1, (0,0,255), thickness = 5)
            contour_list = [] #array que guarda los contornos circulares encontrados
            colors = []
            for con in cnts:
                approx = cv.approxPolyDP(con, 0.1*cv.arcLength(con, True), True) 
                if (len(approx) == 4):
                    x,y,w,h = cv.boundingRect(con)
                    area = cv.contourArea(con)#Rectangle area
                    
                    if w<25 and w > 15 and h<25 and h > 15 and area > 230:
                        cv.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)
                        crop = image[y:y+h,x:x+w]
                        height, width = crop.shape[:2]
                        Color = crop[int(height/2),int(width/2)]
                        #amarillo [1 192 203] [8 158 167]
                        #rojo [0 23 146] [7  35 153]
                        #azul [146 23 0] [136  36   3]
                        #blanco [255 - - ] [-10]
                        #naranja [12 107 255] [5 116 255]
                        #verde [36 100   0]
                        
                        print("Este es el color", Color)
                        cv.imshow("crop", crop)
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
        
     def dibujar(self,mask,color,frame):
         contornos,_ = cv.findContours(mask, cv.RETR_LIST,
         cv.CHAIN_APPROX_NONE)
         #cv.rectangle(imagen,(300,80),(450,230),(0,0,0),-1)
         for c in contornos:
             approx = cv.approxPolyDP(c, 0.1*cv.arcLength(c, True), True) 
             if (len(approx) == 4):
                 area = cv.contourArea(c)
                 if area > 500: 
                     M = cv.moments(c)
                     if (M["m00"]==0): M["m00"]=1
                     #x = int(M["m10"]/M["m00"])
                     #y = int(M['m01']/M['m00'])
                     nuevoContorno = cv.convexHull(c)
                     #cv.circle(frame,(x,y),7,(0,255,0),-1)
                     #cv.putText(frame,'{},{}'.format(x,y),(x+10,y), font, 0.75,(0,255,0),1,cv.LINE_AA)
                     cv.drawContours(frame, [nuevoContorno], 0, color, 3)
         return frame
     
     def get_squares(self):
         while True:
             is_ok, photo = self.cap.read() #adquiero el frame del video
             cv.rectangle(photo,(50,80),(200,230),(0,255,0),1)
             ref_point = [(50,80)]
             ref_point.append((200,230))
             cropped_image = photo[ref_point[0][1]:ref_point[1][1], ref_point[0][0]:
                                                      ref_point[1][0]]
             frameHSV = cv.cvtColor(cropped_image,cv.COLOR_BGR2HSV)
             frameHSV = cv.GaussianBlur(frameHSV, (11, 11), 0) #difuminado, para quitar detalles extras, paso 2
             maskAzul = cv.inRange(frameHSV,azulBajo,azulAlto)
             maskAmarillo = cv.inRange(frameHSV,amarilloBajo,amarilloAlto)
             maskRed = cv.inRange(frameHSV,redBajo1,redAlto1)
             #Dibujando un rectangulo

             if cv.waitKey(1) & 0xFF == ord('c'):
                 cv.imshow('crop_previo',cropped_image)
                #maskRed2 = cv.inRange(frameHSV,redBajo2,redAlto2)
                #maskRed = cv.add(maskRed1,maskRed2)
                 _ = self.dibujar(maskAzul,(255,0,0),cropped_image)
                 _ = self.dibujar(maskAmarillo,(0,255,255),cropped_image)
                 frame_mostrar = self.dibujar(maskRed,(0,0,255),cropped_image)
                 cv.imshow('crop',frame_mostrar)
                 
             cv.imshow('frame',photo)
                 
             
             if cv.waitKey(1) & 0xFF == ord('s'):
               break


font = cv.FONT_HERSHEY_SIMPLEX
