#polygraph via visual

#import libraries
import numpy as np
import cv2
import time

#start face and eye cascades
faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eyeCascade = cv2.CascadeClassifier('haarcascade_eye_tree_eyeglasses.xml')

#create object for camera input via the webcam (0)
videoObject = cv2.VideoCapture(0)
videoObject.set(3,640)
#cap.set(4,480)

def main():
	#initialize globals
	global faceCascade
	global eyeCascade
	global videoObject

	#get start time and setup frame counting variable
	frameCount = 0
	startTime = time.time()

	#variables needed to compute pulse
	pastAverage = 0
	pastBool = False
	pulseCount = 0

	#update variables
	x = 0
	y = 0
	w = 0
	h = 0

	#create / append to output file
	output = open("visual_hb.txt", 'w')

	#keep a iterative loop to continuosly get images from camera to process
	while videoObject.isOpened():
		#capture frame by frame
		ret, frame = videoObject.read()

		#convert to greyscale in order to be used with the haar cascade and find faces
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		faces = faceCascade.detectMultiScale(gray, 1.3, 5)

		#for every face detected
		for (x1,y1,w1,h1) in faces:
			#note 'Regions of Interest' and provide intesity (gray) or bgr color values
			roi_gray = gray[y1:y1+h1, x1:x1+w1]
			roi_color = frame[y1:y1+h1, x1:x1+w1]

			if frameCount % 5 == 0:
				x = x1
				y = y1
				w = w1
				h = h1

		#draw a blue rectangle of brush size 2 around face
		cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 1)

		#area above eyes for pulse
		cv2.rectangle(frame, (x + w/3, y + h/12 + 15), (x + 2*w/3, y + 2*h/12 + 10), (0, 255, 0), 1)

		#get average amount of red in frame
		averagePulse = np.average(frame[y + h/12 + 1 : y + 2*h/12 - 1, x + w/3 +1 : x + 2*w/3 - 1][0][0][2])

		frameCount += 1
		#print str(averagePulse)

		#get fist past frame
		if frameCount == 20:
			pastAverage = averagePulse

		#starting after the first entry check if there is a pulse
		if frameCount >= 21:
			#variability range
			pastAverageL = pastAverage - 0.5
			pastAverageH = pastAverage + 0.7

			#check if pulse (pulse remains for at minimum 2 frames)
			if averagePulse < pastAverageH and averagePulse > pastAverageL and pastBool == False:
				pulseCount = pulseCount + 1
				pastBool =  True
			else:
				pastBool = False

			#reset pastAverage
			pastAverage = averagePulse

			#get data and print
			p = getCamPulse(pulseCount, startTime, frameCount)
			cv2.putText(frame, p, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, .7, (0,0,255))
			cv2.putText(frame, "Press 'Q' to quit.", (50, 70), cv2.FONT_HERSHEY_SIMPLEX, .7, (0,0,255))
			output.write("{}\n".format(p[4:]))

		#display the resulting frame
		cv2.imshow('Webcam Input', frame)


		#break from loop and end display if 'q' is pressed
		if cv2.waitKey(1) & 0xFF == ord('q'):
			print "FPS: " +  str(frameCount / (time.time() - startTime))
			output.close()
			endProgram()

#camera cleanup operations
def endProgram():
	#when everything done, release the capture
	videoObject.release()
	cv2.destroyAllWindows()

	#print goodbye and end program
	print('Bye!')
	sys.exit()

def getCamPulse(pulseCount, startTime, frameCount):
	#get time elapsed
	timeElapsed = time.time() - startTime
	#print("\nTime Elapsed: " + str(timeElapsed) + " seconds.")

	#calculate fps
	fps = frameCount / timeElapsed
	#print("FPS: " + str(fps) + "\n")
	#print("Frame Count: " + str(frameCount) + " Frames.")

	#caluclate bpm
	bpm = pulseCount / timeElapsed * 100
	return ("BPM: " + str(bpm))

#go to main function upon start
if __name__ == '__main__':
	main()