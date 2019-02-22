# coding=utf-8
from __future__ import absolute_import, division

import pprint

import psychopy
import psychopy.gui
import xlrd
from psychopy import core, visual, data, event, logging, clock
import random
import time
import pygame
from psychopy.tools.filetools import fromFile, toFile
import os
import sys
import numpy as np
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle

# upload excel reward structure

file_location = '/Users/ilaria/Desktop/cognitive task/right_left_probabilities.xlsx'
workbook = xlrd.open_workbook(file_location)

# Participant info for everybody
gui = psychopy.gui.Dlg()
gui.addField("Participant Number:", "Ilaria")
gui.addField("Condition Number:", 1)
gui.addField("Age:", 26)
gui.addField("Gender(m/f/o):", "f")
gui.show()

participant_num = gui.data[0]
cond_num = int(gui.data[1])
age = int(gui.data[2])
gender = (gui.data[3])

print(gui.data[3])

# creating and checking file location

data_path = participant_num + "_cond_" + str(cond_num) + "Age" + str(age) + ".tsv"
print("data_path=", data_path)

# time and clocks

clock = psychopy.core.Clock()

if os.path.exists(data_path):
    sys.exit("Data path" + data_path + "already exists!")

responses = []

# setting screen size and images size

print('setting screen size and images size ....')
toy1_size = [200, 200]
toy2_size = [200, 200]
facesad_size = [150, 200]
facehappy_size = [150, 200]
faceneutral_size = [150, 200]
screen_size = [1000, 1000]
# square1_size = [200,200]
# square2_size = [200,200]
gratings_h_size = [200, 200]
gratings_v_size = [200, 200]
fixationcross_size = [50, 50]

# Setup the Window

win = psychopy.visual.Window(
    units='pix',
    size=screen_size,
    fullscr=False,
    # change in True when you run the actual experiment and change the screen size into the actual size of the screen of the pc you will use
    color=[0, 0, 0])

print('setting win...')

print('loading images...')
pos1 = [200, -200]
pos2 = [-200, -200]
rectangle_right = psychopy.visual.Rect(win=win, units="pix", width=toy1_size[0] + 10, height=toy1_size[1] + 10,
                                       lineColor='green', colorSpace='rgb', pos=pos1)
rectangle_left = psychopy.visual.Rect(win=win, units="pix", width=toy2_size[0] + 10, height=toy2_size[1] + 10,
                                      lineColor='green', colorSpace='rgb', pos=pos2)
toy1 = psychopy.visual.ImageStim(win=win, image="toy1_bear.png", color=(1.0, 1.0, 1.0), size=toy1_size, units='pix',
                                 pos=pos1)
toy2 = psychopy.visual.ImageStim(win=win, image="toy2_duck.png", color=(1.0, 1.0, 1.0), size=toy2_size, units='pix',
                                 pos=pos2)
gratings_h = psychopy.visual.ImageStim(win=win, image="gratings_h.png", color=(1.0, 1.0, 1.0), size=gratings_h_size,
                                       units='pix', pos=pos1)
gratings_v = psychopy.visual.ImageStim(win=win, image="gratings_v.png", color=(1.0, 1.0, 1.0), size=gratings_v_size,
                                       units='pix', pos=pos2)
happyface = psychopy.visual.ImageStim(win=win, image="babyhappy2.png", color=(1.0, 1.0, 1.0), size=facehappy_size,
                                      units='pix', pos=[0, 200])
neutralface = psychopy.visual.ImageStim(win=win, image="babyneutral2.png", color=(1.0, 1.0, 1.0), size=faceneutral_size,
                                        units='pix', pos=[0, 200])
sadface = psychopy.visual.ImageStim(win=win, image="babyneg2.png", color=(1.0, 1.0, 1.0), size=facesad_size,
                                    units='pix', pos=[0, 200])
fixation_cross = psychopy.visual.ImageStim(win=win, image="fixation_cross.png", color=(1.0, 1.0, 1.0),
                                           size=fixationcross_size, units='pix', pos=[0, 200])

# one possible luminescent square (arm 1 & 2) Use this instead of square?  SET POSITION 1 AND 2

# print('draw gratings')

# grating = psychopy.visual.GratingStim(
#    win=win,
#    units="pix",
#    size=[100, 100]
# )
# grating.sf = 5.0 / 150.0

# print('draw two gratings')

# orientations = [0.0, 90.0]
# grating_hpos = [-150, 50]

# grating.draw()

# for i_grating in range(2):

#    grating.ori = orientations[i_grating]
#    grating.pos1 = [grating_hpos[i_grating], -200]
#    grating.pos1 = [grating_hpos[i_grating], 200]
#    grating.draw()
# core.wait(5)
# win.flip()

# instructions experimental block of reward condition (earn money)
INSTRUCTIONS_REWARD_EXP = """
        Over the fixation point will be presented a distressed baby face, 
        your task is to soothe the baby with one of the 2 toys available. 
        One of the two is more successful and it will make the baby stop crying or being happy! 
        the other one will not produce any change.
        use left and right arrow to select the toy you think is better and  try to soothe the baby as much as possible!
        Pay attention, the good toy may change!

        Good luck!

        Press 'space' to begin.
        """

# instructions control block of reward condition (earn money)
INSTRUCTIONS_REWARD_CONTR = """
    Over the fixation point will be presented an amount of money 
    (you start with debit condition (-1£) you can extinct your debit (0£) or earn one pound (1£) 
    or stay in debit (-1£)!), 
    your task is to earn the pound as many time as possible with one of the 2 arms available. 
    One of the two is more successful and it will make earn money, 
    the other one might make stay without money or make you loose. 
    use left and right arrow to select the arm you think is successful. 
    Pay attention, the good arm may change!

    Good luck!

    Press 'space' bar to begin.
    """

# instructions experimental block of punishment condition (excite the baby)
INSTRUCTIONS_PUNISHMENT_EXP = """
    Over the fixation point will be presented a neutral baby face, 
    your task is to make the baby happy with one of the 2 toys available. 
    One of the two is more successful and it will make the baby being happy! 
    the other might have no effect or even distress the baby!
    use left and right arrow to select the toy you think is better and  try to make the baby as much as possible!
    Pay attention, the good toy may change!

    Good luck!

    Press 'space' bar to begin.
    """

# instructions control block of punishment condition (not lose money)
INSTRUCTIONS_PUNISHMENT_CONTR = """
    Over the fixation point will be presented an amount of money 
    (you start with debit condition (-1£) you can extinct your debit (0£) or earn one pound (1£) or stay in debit (-1£)!), 
    your task is to earn the pound as many time as possible with one of the 2 arms available. 
    One of the two is more successful and it will make earn money, 
    the other one might make stay without money or make you loose. 
    use left and right arrow to select the arm you think is successful. 
    Pay attention, the good arm may change!

    Good luck!

    Press 'space' bar to begin.
    """

NUM_TRIALS = 200
BANDIT_PROBABILITIES = [0.25, 0.75]

def get_random_toys():
    print()


def get_random_squares():
    print()


def get_random_instructions(instruction_list):
    result = random.choice(instruction_list)
    print(result[0], [1])
    return result[0], result[1]


# add testing

def bandit_task(selected_value, arms, stimuli, feedback, window):
    # define instructions
    # print(messages:["welcome"],["break"],["thanks"])
    print('selected_value is %d' % selected_value)
    instruction_result_text = ""
    if selected_value == 1:
        instruction_result_text, is_exp = get_random_instructions(
            [[INSTRUCTIONS_REWARD_EXP, True], [INSTRUCTIONS_REWARD_CONTR, False]])

    if selected_value == 2:
        instruction_result_text, is_exp = get_random_instructions(
            [[INSTRUCTIONS_PUNISHMENT_EXP, True], [INSTRUCTIONS_PUNISHMENT_CONTR, False]])

    elif selected_value < 1 or selected_value > 2:
        sys.exit("Unknown condition number")

    print('instruction_result is %s and is_exp=%s' % (instruction_result_text, is_exp))

    text_stim_screen = psychopy.visual.TextStim(
        win=window,
        text=instruction_result_text,
        color=(-1, -1, -1), height=30.0)
    text_stim_screen.draw(window)
    win.flip()
    while True:
        print('in while...')
        response = psychopy.event.waitKeys(keyList=['space'])
        print('after response')
        print(response)
        if 'space' in str(response):
            print("selected space!")
            break  # break out of the while-loop

    # experiments
    if is_exp and cond_num == 1:
        experiment_trial(True)

    if is_exp and cond_num == 2:
        experiment_trial(False)

    # add testing
    # control
    if is_exp is False and cond_num == 1:
        control_trial(True)

    if is_exp is False and cond_num == 2:
        control_trial(False)

    print('selected_value is %d' % selected_value)

    # starting screen
    # screen experiments

    if is_exp == True and cond_num == 1 or cond_num == 2:
        print('display fixation cross and arms')
        #   while clock.getTime() < 2.0:
            #draw(fixation_cross)
            #arms, is_exp = get_random_toys([[toy1, True], [toy2, True]])  # they are always random
            #if clock.getTime > 2.0 and cond_num == 1:
            #    draw(sadface)
            #    arms, is_exp = get_random_toys([[toy1, True], [toy2, True]])
            #elif clock.getTime > 2.0 and cond_num == 2:
            #    draw(neutralfaceface)
    #    arms, is_exp = get_random_toys([[toy1, True], [toy2, True]])

    # screen  controls
    if is_exp == False and cond_num == 1 or cond_num == 2:
        print('display fixation cross and arms')
        #while clock.getTime() < 2.0:
        #    draw(fixation_cross)
        #    arms, is_exp = get_random_squares([[gratings_v, True], [gratings_h, True]])  # set gratings
        #    if clock.getTime > 2.0 and cond_num == 1:
        #        draw(text_rule_minusone)
        #        arms, is_exp = get_random_squares([[gratings_v, True], [gratings_h, True]])
        #    elif clock.getTime > 2.0 and cond_num == 2:
        #        draw(text_rule_zero)
        #        arms, is_exp = get_random_squares([[gratings_v, True], [gratings_h, True
                # add testing


def experiment_trial(is_reward):
    print("start experiment trial with is_reward=%s..." % s)
    return 0


# add testing

def control_trial(is_reward):
    print("start control with is_reward=%s..." % s)
    return 0


# add testing

event.globalKeys.clear()

print("start...")

# define welcome, equal across conditions

print ('welcome screen...')
Welcome = "Welcome to our study. Thanks for taking part to this experiment! Press the'SPACE' bar to continue"
text_stim_screen = psychopy.visual.TextStim(
    win=win,
    text=Welcome,
    color=(-1, -1, -1), height=30.0)
text_stim_screen.draw(win)
win.flip()
while True:
    print('in while...')
    response = psychopy.event.waitKeys(keyList=['space'])
    print('response is %s', response)
    print(response)
    if 'space' in response:
        break  # break out of the while-loop

print("condition number is %d." % cond_num)

is_reward ,is_exp = bandit_task(cond_num, None, None, None, win)

# add testing
exit(0)


# dictionary of welcome, break and thanks across conditions
messages = {
    "welcome": "Welcome to our study. Thanks for taking part to this experiment! Press the'SPACE' bar to continue",
    "break": "The first part has been completed! Take some time to rest and press the'SPACE' bar when you are ready to proceed.",
    "thanks": "Congratulations, you have completed the experiment! Thank you for your participation! For any further question, do not hesitate to contact the reseachers."}
if is_reward == False or is_reward == True and is_exp == True or is_exp == False:
    print(messages["welcome"])
    while True:
        print('in while...')
        response = psychopy.event.waitKeys(keyList=['space'])
        print('response is %s', response)
        print(response)
        if 'space' in response:
            break  # break out of the while-loop
    print(messages["break"])
    print(messages["thanks"])
    win.flip()

# dictionary of arms


# Pause for a break every 100 trials

# if trials.thisN % 100 ! = 0:# this isn't trial number 100, 200, 300...
#       continueRoutine = False # so don't run the pause routine this time.

# break screen

take_a_break = "The first part has been completed! Take some time to rest and press the'SPACE' bar when you are ready to proceed."
text_stim_screen = psychopy.visual.TextStim(
    win=win,
    text=take_a_break,
    color=(-1, -1, -1), height=30.0)
while True:
    print('in while...')
    response = psychopy.event.waitKeys(keyList=['space'])
    print('after response')
    print(response)
    if 'space' in response:
        break  # break out of the while-loop

# Thanks screen common across conditions
thanks_message = "Congratulations, you have completed the experiment! Thank you for your participation! For any further question, do not hesitate to contact the reseachers."
text_stim_screen = psychopy.visual.TextStim(
    win=win,
    text=thanks_message,
    color=(-1, -1, -1), height=30.0)

# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)

# restricting the available keys

keys = psychopy.event.waitKeys(keyList=["left", "right", "space"])
win.flip()

# determine when a key is pressed
clock = psychopy.core.Clock()
keys = psychopy.event.waitKeys(timeStamped=clock)
print (keys)
win.flip()

# Store info about the experiment session
expName = 'bandittask'
expInfo = {'participant': '', 'condition': '', 'age': '', 'gender': ''}
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName

# store frame rate of monitor if we can measure it
expInfo['frameRate'] = win.getActualFrameRate()
if expInfo['frameRate'] != None:
    frameDur = 1.0 / round(expInfo['frameRate'])
else:
    frameDur = 1.0 / 60.0  # could not measure, so guess

print("expInfo", expInfo)

# make a text file to save data
fileName = expInfo['participant'] + expInfo['condition'] + expInfo['age'] + expInfo['gender']
dataFile = open(fileName + '.csv', 'w')  # a simple text file with 'comma-separated-values'
dataFile.write('Arrow,ReactionTime,correct\n')  # add info you want to store
dataFile.write("%s, %i, %i" % ())

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + u'data/%s_%s_%s' % (expInfo['participant'], expName, expInfo['date'])

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
                                 extraInfo=expInfo, runtimeInfo=None,
                                 originPath='/Users/ilaria/Desktop/cognitive task/python_bandit.py',
                                 # define path you'll use at experimental psychology
                                 savePickle=True, saveWideText=True,
                                 dataFileName=filename)

# save a log file for detail verbose info
logFile = logging.LogFile(filename + '.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

# endExpNow = False  # flag for 'escape' or other condition => quit the exp


# background and images size settings  all conditions
print('draw image')

# images settings control condition

print('loading controls...')
text_rule_zero = "0 £"
text_stim_screen = psychopy.visual.TextStim(
    win=win,
    text=text_rule_zero,
    color=(-1, -1, -1), pos=[0, 200])

# text_stim_screen.draw(win)

win.flip()
text_rule_one = "1 £"
text_stim_screen = psychopy.visual.TextStim(
    win=win,
    text=text_rule_one,
    color=(-1, -1, -1), pos=[0, 200])

# text_stim_screen.draw(win)

win.flip()
text_rule_minusone = "-1 £"
text_stim_screen = psychopy.visual.TextStim(
    win=win,
    text=text_rule_minusone,
    color=(-1, -1, -1), pos=[0, 200])

win.flip()

# arms settings control condition

print('loading control arms...')
trialClock = core.Clock()
# square1 = psychopy.visual.ImageStim(win=win, image="square1.png", color=(1.0, 1.0, 1.0), size=square1_size, units='pix', pos=pos1)
# square2 = psychopy.visual.ImageStim(win=win, image="square2.png", color=(1.0, 1.0, 1.0), size=square2_size, units='pix', pos=pos2)
grating1 = psychopy.visual.ImageStim(win=win, image="gratings_h.png", color=(1.0, 1.0, 1.0), size=gratings_h_size,
                                     units='pix', pos=pos1)
grating2 = psychopy.visual.ImageStim(win=win, image="gratings_v.png", color=(1.0, 1.0, 1.0), size=gratings_v_size,
                                     units='pix', pos=pos2)

print('draw squares...')

# add functions for probabilities underlying successul feedback.

# win.flip()

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine

# keep track of the time
print('track time...')
globalClock = core.Clock()
trialClock = core.Clock()

# trials

clock = psychopy.core.Clock()
n_trials = 200
pre_duration_s = 0.5  # wait before sghowing the stimuli 500 ms
stim_duration_s = 3

# def gender

print('define gender')
if gender == "m":
    print("You chose male")
elif gender == "f":
    print("You chose female")
elif gender == "o":
    print("You chose other")
else:
    sys.exit("Unknown gender")

# define function for the task


# cleaning up, closing the window and experiment

win.close()
core.quit()

# define bits of coding that differ across conditions


# draw baseline images condition 1 experimental

core.wait(0.5)
print('fixation cross!')
fixation_cross.draw(win)
toy1.draw(win)
toy2.draw(win)
core.wait(0.2)
sadface.draw(win)

# draw what you need for condition one on the screen


# set stimuli response (if select toy successful draw happy/neutral face 50%) if select unsuccessful give sad
# register response L=1 R=2, use arrows

# psychopy.event.waitKeys()
# keys = psychopy.event.getKeys(
# keyList=["left", "right"],
# timeStamped=clock
# )

# for key in keys:

# if key[0] == "left":
# key_num = 1
# else:
# key_num = 2

# responses.append([key_num, key[1]])


# data = []

# for trial in range(10):  #10 trails now, how many do we want?

# data.append(
# [
# random.uniform(0, 180),
# random.choice(["left", "right"])
# ]
# )

# pprint.pprint(data)

# coded_data = []

# for data_row in data:

# if data_row[1] == "left":
# data_row[1] = 1
# elif data_row[1] == "right":
# data_row[1] = 2

# coded_data.append(data_row)

# pprint.pprint(coded_data)

# np.savetxt(data_path, responses, delimiter="\t")

# win.close()

# break screen

text_rule_break = """
    The first part has been completed! Take some time to rest and press the'SPACE' bar when you are ready to proceed.
    """
text_stim_screen = psychopy.visual.TextStim(
    win=win,
    text=text_rule_break,
    color=(-1, -1, -1), height=30.0)

text_stim_screen.draw(win)
win.flip()

while True:
    print('in while...')
    response = psychopy.event.waitKeys(keyList=['space'])
    print('after response')
    print(response)
    if 'space' in response:
        break  # break out of the while-loop
'''
'''
while True:
    print('in while...')
    response = psychopy.event.waitKeys()  # you probably have event.waitKeys(keyList=['space']) or something like that right now
    print('after response')
    print(response)
    if 'left' in response:
        left = True
        right = False
        break  # break out of the while-loop
    if 'right' in response:
        right = True
        left = False
        break  # break out of the while-loop

# print("left=%s , right=%s"% (left, right))

toy1.setPos(pos2)
toy2.setPos(pos1)
'''
print("position setted")
'''

psychopy.event.waitKeys()

keys = psychopy.event.getKeys(
    keyList=["left", "right"],
    timeStamped=clock
)

for key in keys:

    if key[0] == "left":
        key_num = 1
    else:
        key_num = 2

    responses.append([key_num, key[1]])

data = []

for trial in range(10):  # 10 trails now, how many do we want?

    data.append(
        [
            random.uniform(0, 180),
            random.choice(["left", "right"])
        ]
    )

pprint.pprint(data)

coded_data = []

for data_row in data:

    if data_row[1] == "left":
        data_row[1] = 1
    elif data_row[1] == "right":
        data_row[1] = 2

    coded_data.append(data_row)

pprint.pprint(coded_data)

np.savetxt(data_path, responses, delimiter="\t")

# win.close()

trials = None
# end a loop
trials.finished = True

# Pause for a break every 100 trials
if trials.thisN % 100 != 0:  # this isn't trial number 100, 200, 300...
    continueRoutine = False  # so don't run the pause routine this time.

# break screen
text_rule = "The first part has been completed! Take some time to rest and press the'SPACE' bar when you are ready to proceed."
text_stim_screen = psychopy.visual.TextStim(
    win=win,
    text=text_rule,
    color=(-1, -1, -1), height=30.0)

while True:
    print('in while...')
    response = psychopy.event.waitKeys(keyList=['space'])
    print('after response')
    print(response)
    if 'space' in response:
        win.flip()
        # break  #break out of the while-loop


# add function core.wait() to tell to waits for the amount of time we want in seconds


# Instructions condition 2 EXPERIMENTAL (make the baby happy)


# for key in keys:

#  if key[0] == "left":
#     key_num = 1
# else:
#   key_num = 2

# responses.append([key_num, key[1]])

#    data = []

#    for trial in range(10): #10 trails now, how many do we want?

#        data.append(
#            [
#                random.uniform(0, 180),
#                random.choice(["left", "right"])
#           ]
#       )

#    pprint.pprint(data)

#    coded_data = []

#    for data_row in data:

#        if data_row[1] == "left":
#            data_row[1] = 1
#        elif data_row[1] == "right":
#            data_row[1] = 2

#        coded_data.append(data_row)

#    pprint.pprint(coded_data)

#   np.savetxt(data_path, responses, delimiter="\t")

#   win.close()


# psychopy.event.waitKeys()
# clock = psychopy.core.Clock()
# keys = psychopy.event.waitKeys(keyList=["left", "right"])
# keys = psychopy.event.waitKeys(timeStamped=clock)

# print(keys)

# win.close()

# for key in keys:

#       if key[0] == "left":
#          key_num = 1
#     else:
#        key_num = 2

#   responses.append([key_num, key[1]])


# data = []

#   for trial in range(10):  #10 trails now, how many do we want?

#       data.append(
#          [
#             random.uniform(0, 180),
#            random.choice(["left", "right"])
#        ]
#    )

# pprint.pprint(data)

# coded_data = []

#   for data_row in data:

#      if data_row[1] == "left":
#         data_row[1] = 1
#    elif data_row[1] == "right":
#        data_row[1] = 2

#   coded_data.append(data_row)

# pprint.pprint(coded_data)

# np.savetxt(data_path, responses, delimiter="\t")

# win.close()

# link to xlsx file


# position []
# answer=xlrd.open_workbook(r'answer.xlsx')
# sheet=answer.sheet_by_index(0)

# save data in excel with labels

# Thanks screen common across conditions

#  text_rule_thanks= """
# Congratulations, you have completed the experiment! Thank you for your participation! For any further question, do not hesitate to contact the reseachers.
# """
# text_stim_screen=psychopy.visual.TextStim(
# win=win,
# text=text_rule_thanks,
# color=(-1,-1,-1), height=30.0)

# cleaning up, closing the window and experiment

# win.close()
# core.quit()


def main():
    print("python main function")


if __name__ == '__main__':
    main()
