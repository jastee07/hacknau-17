import time
import pyaudio
import numpy as np

#create values for sound recording
maxNoise = 0

def main():
	getSpeechDelay('calibrate')
	getSpeechDelay('run')

def getSpeechDelay(calibrate_or_run):
	#initialize global variables
	global maxNoise
	silence_startTime = time.time()
	silence_length = 0
	itsLoud = True

	#create pyAudio object to get microphone input
	p = pyaudio.PyAudio()
	stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=2**11)

	#set 'maxNoise' variable to loudest ambient sound in calibration
	if (calibrate_or_run == 'calibrate'):
		print "Calibrating microphone..."

		#~20 samples takes 1 second, calibrate for 5 seconds
		for i in range(int(20 * 5)):
			data = np.fromstring(stream.read(2**11), dtype=np.int16)
			value = np.average(np.abs(data))*2

			if value > maxNoise:
				maxNoise = value	

		print "Calibration complete!"
	else: 
		#create / append to output file
		output = open("speech_delay.txt", 'w')

		#~20 samples takes 1 second, calibrate for 5 seconds
		while True:
			data = np.fromstring(stream.read(2**11), dtype=np.int16)
			value = np.average(np.abs(data))*2

			if value < maxNoise and itsLoud:
				silence_startTime = time.time()
				itsLoud = False
				output.write("{}\n".format(silence_length))
			elif value > maxNoise * 1.2:
				silence_length = time.time() - silence_startTime
				itsLoud = True

		output.close()

	#end and close streams / pyAudio
	stream.stop_stream()
	stream.close()
	p.terminate()

#go to main function upon start
if __name__ == '__main__':
	main()