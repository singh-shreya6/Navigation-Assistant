import speech_recognition as sr
import pyttsx3
import os
import time
from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import argparse
import imutils
import time
import cv2
import math


def objectdetection(objname):
	ap = argparse.ArgumentParser()
	ap.add_argument("-p", "--prototxt", required=True,
		help="path to Caffe 'deploy' prototxt file")
	ap.add_argument("-m", "--model", required=True,
		help="path to Caffe pre-trained model")
	ap.add_argument("-c", "--confidence", type=float, default=0.2,
		help="minimum probability to filter weak detections")
	args = vars(ap.parse_args())

	CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
		"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
		"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
		"sofa", "train", "tvmonitor"]

	COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

	print("[INFO] loading model...")
	net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])
	print("Model information obtained")

	print("[INFO] starting video stream...")
	vs = VideoStream(src=0).start()
	time.sleep(2.0)
	fps = FPS().start()

	frame_width = 600
	user_x = frame_width/2
	user_y = frame_width

	while True:
		frame = vs.read()
		frame = imutils.resize(frame,width=frame_width)

		(h, w) = frame.shape[:2]
		blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)),
			0.007843, (300, 300), 127.5)

		net.setInput(blob)
		detections = net.forward()
		fl=False
		for i in np.arange(0, detections.shape[2]):
			confidence = detections[0, 0, i, 2]

			if confidence > args["confidence"]:

				idx = int(detections[0, 0, i, 1])
				if objname in CLASSES[idx] :
					fl=True
					box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
					(startX, startY, endX, endY) = box.astype("int")

					label = "{}: {:.2f}%".format(CLASSES[idx],
						confidence * 100)
					cv2.rectangle(frame, (startX, startY), (endX, endY),
						COLORS[idx], 2)
					y = startY - 15 if startY - 15 > 15 else startY + 15
					cv2.putText(frame, label, (startX, y),
						cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)
	#				print("StartX ",startX)
	#				print("EndX ",endX)
	#				print("StartY ",startY)
	#				print("EndY ",endY)
					centerX = (endX+startX)/2
					centerY = (endY+startY)/2
		#			print("CenterX ",centerX)
		#			print("CenterY ",centerY)
					cv2.line(frame,(int(user_x),int(user_y)),(int(centerX),int(centerY)),(255,0,0),7)
					dir =0
					if centerX > user_x :
						dir =1
					elif centerX < user_x :
						dir = -1
					deg = math.degrees(math.atan(abs(centerX-user_x)/abs(centerY-user_y)))
					

		cv2.imshow("Frame", frame)
		
		key = cv2.waitKey(1)  & 0xFF

		if key == ord("q"):
			break
		
		fps.update()

	fps.stop()
	print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
	print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

	cv2.destroyAllWindows()
	vs.stop()
	return fl,deg,dir

				


duration = 0.5
freq = 440
engine = pyttsx3.init()
engine.setProperty('rate', 150)
#engine.setProperty('voice', 'english+f1')
def beep() :
	os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % (duration, freq))
engine.say("Welcome to sabre navigation assistant. Speak help me to activate")
engine.say("sabre")
engine.runAndWait()
r = sr.Recognizer()
with sr.Microphone() as source:
		wakeup = False
		r.adjust_for_ambient_noise(source)
		wakeString = r.listen(source)
		wakeStringFinal = ""
		try:
			wakeStringFinal = r.recognize_google(wakeString)
		except:
			wakeStringFinal= "help me"
		if wakeStringFinal == "help me" :
			count = 0
			wakeup = True
			while count<5 and wakeup == True:
				beep()
				audio = r.listen(source)
				try:
					query = r.recognize_google(audio)
					print(query)
					if query == "bye":
						wakeup = False
						engine.say("bye")
						engine.runAndWait()
						break
					l= query.split()
					print 
					k = l[0]
					secondArg = l[1]
					if "bottle" in l:
						secondArg="bottle"
					elif "chair" in l:
						secondArg="chair"
					
					print (k)
					print (secondArg)
					if (k=="find"):
						print("you are finding something")
						print(secondArg)
						engine.say("searching for")
						engine.runAndWait()
						engine.say(secondArg)
						engine.runAndWait()
						found = False
						found,deg,dir=objectdetection(secondArg)
						if found== True:
							print("object found")
							direction = "ahead"
							if dir ==-1:
								direction = "left"
							elif dir ==1:
								direction = "right"
							st=str(secondArg)+" found at "+str(int(deg))+" Degree "+str(direction)
							print(st)
							engine.say(st)
							
							engine.runAndWait()
							wakeup = False
						else :
							print("could not find try again")
							time.sleep(1)
							engine.say("Could not find try again")
							engine.runAndWait()
							count+=1



				except:
					time.sleep(3)
					count +=1;
