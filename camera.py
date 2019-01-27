# python camera.py

#from pyimagesearch.centroidtracker import CentroidTracker
from keras.preprocessing.image import img_to_array
from keras.models import load_model
from imutils.video import VideoStream
import numpy as np
import imutils
import time
import cv2
import os
import argparse
import datetime
import random

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
args = vars(ap.parse_args())

TOTAL_CONSEC = 0
TOTAL_THRESH = 20

DRONE = False

CAM_ID = '0'

# print("[INFO] starting video stream...")
# vs = VideoStream(src=0).start()
# # vs = VideoStream(usePiCamera=True).start()
# time.sleep(2.0)
#
# if args.get("video", None) is None:
# 	vs = VideoStream(src=0).start()
# 	time.sleep(2.0)
# else:
# vs = cv2.VideoCapture('./videos/example_02.mp4')

print("[INFO] loading model...")
model = load_model('./node-drone.model')

print("[INFO] starting video stream...")
vs = VideoStream(src=1).start()
# vs = VideoStream(usePiCamera=True).start()
time.sleep(2.0)
# model = load_model('./node-drone.model')

firstFrame = None

def alert_on_drone (img):
	d = datetime.datetime.now().strftime("%A-%d-%B-%Y-%I-%M-%S%p")
	print('DRONE DETECTED')
	print(d)
	cv2.imwrite('./raw/'+CAM_ID+'_'+d+'.png', img)

while True:
	frame = vs.read()
	frame = frame if args.get("video", None) is None else frame[1]
	text = "no tracks"
	if frame is None:
		break
	frame = imutils.resize(frame, width=500)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (21, 21), 0)
	if firstFrame is None or random.randint(0, 1000) < 5:
		firstFrame = gray
		continue
	frameDelta = cv2.absdiff(firstFrame, gray)
	thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
	thresh = cv2.dilate(thresh, None, iterations=2)
	cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	for c in cnts:
		if cv2.contourArea(c) < args["min_area"]:
			continue
		(x, y, w, h) = cv2.boundingRect(c)
		text = "tracking"
		# yishimish
		if w > 400:
			continue
		nframe = frame[y:x, (y + h):(x + w)]
		if nframe is None or nframe.shape[0] == 0 or nframe.shape[1] == 0:
			continue
		# nframe = imutils.resize(nframe, width=400)
		nimage = cv2.resize(nframe, (28, 28))
		nimage = nimage.astype("float") / 255.0
		nimage = img_to_array(nimage)
		nimage = np.expand_dims(nimage, axis=0)
		(notDRONE, DRONE) = model.predict(nimage)[0]
		label = "Not Drone"
		proba = notDRONE
		if DRONE > notDRONE:
			label = "Drone"
			proba = DRONE
			TOTAL_CONSEC += 1
			if not DRONE and TOTAL_CONSEC >= TOTAL_THRESH:
				DRONE = True
		else:
			TOTAL_CONSEC = 0
			DRONE = False
		if label == 'Drone':
			alert_on_drone (nframe)
		label = "{}: {:.2f}%".format(label, proba * 100)

		# frame = cv2.putText(frame, label, (x, y),
			# cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

	for c in cnts:
		if cv2.contourArea(c) < args["min_area"]:
			continue
		(x, y, w, h) = cv2.boundingRect(c)
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

	cv2.imwrite('./feed/'+CAM_ID+'_latest.png', frame)

	cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
		(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

	# nframe = imutils.resize(frame, width=400)
	# nimage = cv2.resize(nframe, (28, 28))
	# nimage = nimage.astype("float") / 255.0
	# nimage = img_to_array(nimage)
	# nimage = np.expand_dims(nimage, axis=0)
	# (notDRONE, DRONE) = model.predict(nimage)[0]
	# label = "Not Drone"
	# proba = notDRONE
	# if DRONE > notDRONE:
	# 	label = "Drone"
	# 	proba = DRONE
	# 	TOTAL_CONSEC += 1
	# 	if not DRONE and TOTAL_CONSEC >= TOTAL_THRESH:
	# 		DRONE = True
	# else:
	# 	TOTAL_CONSEC = 0
	# 	DRONE = False
	# if label == 'Drone':
	# 	alert_on_drone (frame)
	# label = "{}: {:.2f}%".format(label, proba * 100)
	# frame = cv2.putText(frame, label, (10, 25),
		# cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
	#cv2.imshow("Security Feed", frame)
	key = cv2.waitKey(1) & 0xFF
	if key == ord("q"):
		break

vs.stop() if args.get("video", None) is None else vs.release()
cv2.destroyAllWindows()
