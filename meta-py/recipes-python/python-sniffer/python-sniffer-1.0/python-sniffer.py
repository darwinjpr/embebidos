#!/usr/bin/env python

#Import necesary libraries
import cv2
import numpy as np

#Capture video from webcam
cap = cv2.VideoCapture(0)

#Writes the output in the footage.avi file
out = cv2.VideoWriter('footage.avi', cv2.VideoWriter_fourcc(*'MJPG'), 30.0, (856,480))

#Captures two frames from the webcam video
_, frame = cap.read()
_, postframe = cap.read()

while (True):
	#Resize frames
	#frame = cv2.resize(frame, (856,480))
	#postframe = cv2.resize(postframe, (856,480))
	
	#Capture movement in the video
	diff = cv2.absdiff(frame, postframe)
	
	#Reformat video for better performance
	gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
	blur = cv2.GaussianBlur(gray, (5,5), 0)
	_, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
	
	#Processing for sharp contours
	dilated = cv2.dilate(thresh, None, iterations=3)
	_, contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

	#Creates the contours
	for contour in contours:
		(x, y, w, h) = cv2.boundingRect(contour)
		
		#Reduce noise and save video with detected movement
		if cv2.contourArea(contour) > 500:
			out.write(frame.astype('uint8'))
	
	#Display the video
	cv2.imshow("Frame", frame)
	
	frame = postframe
	_, postframe = cap.read()
	
	#Ends the program
	key = cv2.waitKey(1)
	if key == 27: break

cap.release()
out.release()
cv2.destroyAllWindows()

"""
	Tomar foto con Python y opencv
	@date 20-03-2018
	@author parzibyte
	@see https://www.parzibyte.me/blog


import cv2
import uuid


	En este caso, 0 quiere decir que queremos acceder
	a la cámara 0. Si hay más cámaras, puedes ir probando
	con 1, 2, 3...

cap = cv2.VideoCapture(0)

leido, frame = cap.read()

if leido == True:
	nombre_foto = str(uuid.uuid4()) + ".png" # uuid4 regresa un objeto, no una cadena. Por eso lo convertimos
	cv2.imwrite(nombre_foto, frame)
	print("Foto tomada correctamente con el nombre {}".format(nombre_foto))
else:
	print("Error al acceder a la cámara")


	Finalmente liberamos o soltamos la cámara

cap.release()
"""
