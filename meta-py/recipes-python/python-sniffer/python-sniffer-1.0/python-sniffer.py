#Import necesary libraries
import cv2
import numpy as np
from datetime import date
from datetime import datetime, timedelta

#Define variables
contador = 1
Primero = True
No_registrado = True
end = datetime.now()

#Function for headline
def headline():
	file = open("Informe.txt","a+")
	file.write("Lista de intrusiones detectadas\n\n")
	file.close()
	return 0

#Function for report file
def report(now,marca,cont):
	file = open("Informe.txt","a+")

	file.write("Numero de intrusion: {}\n".format(cont))
	file.write("Clasificacion: "+marca+"\n")
	file.write("Fecha: {}/{}/{}\n".format(now.day, now.month, now.year))
	file.write("Hora: {}:{}\n".format(now.hour, now.minute))
	file.write("\n------------------\n\n")

	file.close()
	return cont + 1

#Write headline
headline()

#Initialize person detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

#Capture video from webcam
cap = cv2.VideoCapture(0)

#Writes the output in the footage.avi file
out = cv2.VideoWriter('footage.avi', cv2.VideoWriter_fourcc(*'MJPG'), 24.0, (480,360))

#Captures two frames from the webcam video
_, frame = cap.read()
_, postframe = cap.read()

while (True):

	#Resize frames
	frame = cv2.resize(frame, (480,360))
	postframe = cv2.resize(postframe, (480,360))
	
	#Capture movement in the video
	diff = cv2.absdiff(frame, postframe)
	
	#Reformat video for better performance
	gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
	blur = cv2.GaussianBlur(gray, (5,5), 0)
	_, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
	
	#Creates the contours
	_, contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	
	#Detect motion based on contours
	for contour in contours:
		if cv2.contourArea(contour) > 400:
			fecha = datetime.now()
			end = fecha + timedelta(seconds=3)

			#Checks if it is a new intrusion
			if Primero:
				Primero = False
				reference = fecha + timedelta(seconds=3)
			
			elif fecha >= reference and not Primero and No_registrado:
				#Initialize algoritm to differentiate people from animals
				gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
				boxes, _ = hog.detectMultiScale(gray, winStride=(4,4), scale=1.1)
				if len(boxes) != 0:
					indicador = "Persona"
				else:
					indicador = "Animal"
			
				#Sumits report
				contador = report(fecha,indicador,contador)
				No_registrado = False
			else:
				continue

			break
	
	#Checks moment of last detected movement
	ahora = datetime.now()
	if ahora >= end and not Primero:
		Primero = True
		No_registrado = True
	
	#Display and safe the video
	cv2.imshow("Frame", frame)
	out.write(frame.astype('uint8'))
	
	#Captures the next frames
	frame = postframe
	_, postframe = cap.read()
	
	#Ends the program
	key = cv2.waitKey(1)
	if key == 27: break

cap.release()
out.release()
cv2.destroyAllWindows()
