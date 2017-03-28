import numpy as np
import cv2

#bottle_cascade = cv2.CascadeClassifier('train_classifier/classifier_1/classifier/cascade.xml')
#bottle_cascade = cv2.CascadeClassifier('classifier_2/classifier/cascade.xml')
juice_cascade = cv2.CascadeClassifier('classifier_3/classifier/cascade.xml')
bottle_cascade = cv2.CascadeClassifier('classifier_2_resized/classifier/cascade.xml')
cap = cv2.VideoCapture(0)

while(1):
	ret,frame = cap.read()

	# resize, scaled by target width
	target_width = 600.0
	r = target_width / frame.shape[1]
	dim = (int(target_width), int(frame.shape[0] * r))
	frame_resized = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
	#frame_resized = cv2.flip(frame_resized, 1)
	# get greyscale image
	frame_grey = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2GRAY)
	
	# apply cascade classifier
	detected_bottles = bottle_cascade.detectMultiScale(frame_grey, 1.05, 8)
	for (x,y,w,h) in detected_bottles:
		# draw rect around bottle: image, top left point, bottom right point
		w_shift = int(w * 0.3)
		h_shift = int(h * 0.1)
		cv2.rectangle(frame_resized, (x+w_shift, y+h_shift), (x+w-w_shift, y+h+h_shift), (255,0,0), 1)
		cv2.putText(frame_resized, "vodka", (x+w_shift,y+20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255))
	
	# apply second cascade classifier
	detected_juice = juice_cascade.detectMultiScale(frame_grey, 1.05, 8)
	for (x,y,w,h) in detected_juice:
		# draw rect around bottle: image, top left point, bottom right point
		w_shift = int(w * 0.3)
		h_shift = int(h * 0.1)
		cv2.rectangle(frame_resized, (x+w_shift, y+h_shift), (x+w-w_shift, y+h+h_shift), (0,255,0), 1)
		cv2.putText(frame_resized, "juice", (x+w_shift,y+20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255))
		
	cv2.imshow('bottle detector', frame_resized)
	
	# wait for 5 seconds before closing frame
	if cv2.waitKey(5) == 27:
		break

cv2.destroyAllWindows()
