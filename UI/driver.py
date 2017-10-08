import matplotlib.pyplot as plt
import matplotlib.animation as animation

#style.use('fivethirtyeight')


fig = plt.figure(1)
vis_axl = fig.add_subplot(3,1,1)

spe_axl = fig.add_subplot(3,1,2)

ard_axl = fig.add_subplot(3,1,3)


def animate(i):
	visual_data = open('./visual_hb.txt', 'r').read()
	speech_data = open('./speech_delay.txt', 'r').read()
	arduino_data = open('./arduino_temp.txt', 'r').read()
	visual_lines = visual_data.split('\n')
	speech_lines = speech_data.split('\n')
	temp_lines = arduino_data.split('\n')
	vx_count = 0
	vs_count = 0
	temp_count = 0
	visual_x = []
	visual_y = []
	speech_x = []
	speech_y = []
	arduino_x = []
	arduino_y = []
	for vis_y in visual_lines:
		visual_y.append(vis_y)
		visual_x.append(vx_count)
		vx_count += 1
	for spe_y in speech_lines:
		speech_y.append(spe_y)
		speech_x.append(vs_count)
		vs_count += 1
	for ard_y in temp_lines:
		arduino_y.append(ard_y)
		arduino_x.append(temp_count)
		temp_count += 1

	if len(visual_y) > 50:
		visual_y.pop(0)
		visual_x.pop(0)
	if len(speech_y) > 50:
		speech_y.pop(0)
		speech_x.pop(0)
	if len(arduino_y) > 50:
		arduino_y.pop(0)
		arduino_x.pop(0)

	vis_axl.clear()
	spe_axl.clear()
	ard_axl.clear()
	vis_axl.plot(visual_x, visual_y)
	spe_axl.plot(speech_x, speech_y)
	ard_axl.plot(arduino_x, arduino_y)
	vis_axl.set_title("Visual Indicator")
	spe_axl.set_title("Auditory Indicator")
	ard_axl.set_title("Temperature Indicator")
ani = animation.FuncAnimation(fig, animate, interval=200)
plt.show()
