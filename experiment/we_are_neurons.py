from psychopy import core, visual, event
from matplotlib import pyplot as plt
from PIL import Image
import datetime as dt
import seaborn as sns
import pandas as pd
import numpy as np

# settings
reps_per_cond = 3

# create a window instance
win = visual.Window(fullscr=True)
# create welcome message
welcome = 'Welcome to the neuron experiment!'
txt = visual.TextStim(win, text=welcome, units='norm', \
	height=0.1)

# draw welcome message
txt.draw()
win.flip()
# wait for response
k = event.waitKeys()

# prepare - close eyes, position hands
text = "Ok, let's start. Get in your positions and close your eyes, neurons."
txt.setText(text)
txt.draw()
win.flip()

# setup of info screen
filename = 'test.png'
all_times = np.array([])
figsizes = [(550, 800)]
condition_list = np.array([])

Time1 = visual.TextStim(win, units='norm', height=0.1, pos=(0, 0.8))
Time2 = visual.TextStim(win, units='norm', height=0.1, pos=(0, 0.6))
current_time_text = 'Recorded travel time:  '
mean_time_text = 'Mean travel time:  '

# setup subplots
f, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
info_img = visual.ImageStim(win, image=None,  
            pos=(0, -100), size=figsizes[0], units = 'pix')


# start measuring time after key press

condtext = ["Now prepare for condition 2", "Now - comparison of two conditions"]
for c in range(0, 2):
	for t in range(reps_per_cond):
		k = event.waitKeys()
		t1 = core.getTime()
		k = event.waitKeys(timeStamped=True)
		t2 = k[0][1]
		recorded_time = t2 - t1
		all_times = np.append(all_times, recorded_time)

		# set text
		Time1.setText(current_time_text + '{:.4f}'.format(recorded_time))	
		Time2.setText(mean_time_text + '{:.4f}'.format(all_times.mean()))	
		Time1.draw()
		Time2.draw()

		# plot things...
		scatter_x_ax = np.ones(len(all_times))
		ax1.scatter(scatter_x_ax, all_times, s=16)
		ax2.plot(all_times)
		ax1.set_ylim(all_times.min()-0.2, all_times.max()+0.2)
		ax1.set_xlim(0.9, 1.1)
		ax1.set_title('Scattered travel times')
		ax2.set_title('History of travel times')
		ax2.set_xlim(0, len(all_times))
		f.savefig(filename)

		ax1.clear()
		ax2.clear()

		# load the figure
		img = Image.open(filename)
		imgsize = np.array(img.size)
		del img

		# set image
		info_img.size = imgsize
		info_img.setImage(filename)
		info_img.draw()
		win.flip()

	# pack all_times into conditions_list
	condition_list = np.append(condition_list, all_times)
	all_times = np.array([])

	k = event.waitKeys()
	txt.setText(condtext[c])
	txt.draw()
	win.flip()

k = event.waitKeys()

# compare conditions
# ------------------

# create a data frame
data_dict = {'travel time' : condition_list, 'body part' : \
	['shoulder'] * reps_per_cond + ['leg'] * reps_per_cond}
df = pd.DataFrame(data_dict)

# set figure style
sns.set(style="ticks")

# create figure
g = sns.factorplot("body part", "travel time", data=df, kind="box",
                   palette="PRGn")
g.despine(offset=10, trim=True)
# save figure
plt.savefig(filename)

# get image on screen
img = Image.open(filename)
imgsize = np.array(img.size)
del img

# set image
info_img.size = imgsize
info_img.setImage(filename)
info_img.draw()
win.flip()

# save dataframe
tm = dt.datetime.now()
tm = tm.strftime('%H.%M')
df.to_csv('data_'+tm+'.scv')

k = event.waitKeys()

core.quit()

