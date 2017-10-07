#get pulse of person in frame
#also prints out number of faces in frame
#import stuff
import numpy as np
import cv2
import sys
import time

#start face and eye cascades
faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eyeCascade = cv2.CascadeClassifier('haarcascade_eye_tree_eyeglasses.xml')

#after a few minutes a recursion limit is hit, try with iteration or increase recursion limit
#sys.setrecursionlimit(1000)		#no longer needed

#create object for camera input via the webcam (0)
videoObject = cv2.VideoCapture(0)

#font for writing on display
font = cv2.FONT_HERSHEY_SIMPLEX

def endProgram():
	#get end time
    endTime = time.time()

    #when everything done, release the capture
    videoObject.release()
    cv2.destroyAllWindows()

    #print goodbye and end program
    print('Bye!')
    sys.exit()

def averageRed(targetFrame):
	#find the average red value in the frame
	averageCOR = np.average(targetFrame, axis = 0)
	averageColor = np.average(averageCOR, axis = 0)

	#return the average colors (bgr) on the frame
	return (averageColor[2])

def getPulse(pulseCount, startTime, frameCount):
	#get time elapsed
    timeElapsed = time.time() - startTime
    #print("\nTime Elapsed: " + str(timeElapsed) + " seconds.")

    #calculate fps
    fps = frameCount / timeElapsed
    #print("FPS: " + str(fps) + "\n")
    #print("Frame Count: " + str(frameCount) + " Frames.")

    #caluclate bpm
    bpm = pulseCount / timeElapsed * 100
    print("BPM: " + str(bpm))
    return bpm
    

def main():
	#find opencv version
    (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')

    #get start time and setup frame counting variable
    frameCount = 0
    startTime = time.time()

    #variables needed to compute pulse
    pastAverage = 0
    pastBool = False
    pulseCount = 0

    #keep a iterative loop to continuosly get images from camera to process
    while videoObject.isOpened():
    	#capture frame by frame
    	ret, frame = videoObject.read()

        #convert to greyscale in order to be used with the haar cascade and find faces
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.3, 5)

        print("Number of Faces in screen: " + str(len(faces)))

        #for every face detected
        for (x,y,w,h) in faces:
            #draw a blue rectangle of brush size 2 around face
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 1)

            #note 'Regions of Interest' and provide intesity (gray) or bgr color values
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = frame[y:y+h, x:x+w]

            #use cascades to find eyes WITHIN the face image (no random eyeballs)
            eyes = eyeCascade.detectMultiScale(roi_gray)
            for (ex, ey, ew, eh) in eyes:
            	#eyes
                cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

                #area beneath eyes fr pulse
                cv2.rectangle(roi_color, (ex + ew/2, ey + 140), (ex + ew/2 + 25, ey + 125), (255, 0, 0), 2)

                #get changes in the color values of camera
                averagePulse = averageRed(frame[y + ey + 115:y + ey + 140, x + ex + ew/2:x + ex + ew/2 + 25])
                #print(str(x))

                #get fist past frame
                if frameCount == 20:
                	pastAverage = averagePulse

                #starting after the first entry check if there is a pulse
                if frameCount >= 21:
                	#checkPulse()
                	#variability range
                	pastAverageL = pastAverage - 0.5
                	pastAverageH = pastAverage + 0.5

                	#check if pulse (pulse remains for at minimum 2 frames)
                	if averagePulse < pastAverageH and averagePulse > pastAverageL and pastBool == False:
                		pulseCount = pulseCount + 1
                		pastBool =  True
                	else:
                		pastBool = False

                	#reset pastAverage
                	pastAverage = averagePulse

                	p = getPulse(pulseCount, startTime, frameCount)
                	display = "BPM: " + str(p)
                	#cv2.putText(frame, display, (10, 50), font, 2, (255,255,255), 2, cv2.LINE_AA)
                	print(str(p))

                #increment frame counter variable
                frameCount = frameCount + 1

    
        #display the resulting frame
        cv2.imshow('Webcam Input', frame)

        #break from loop and end display if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            endProgram()

if __name__ == '__main__':
    main()
