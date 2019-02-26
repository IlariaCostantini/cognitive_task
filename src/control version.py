from __future__ import absolute_import, division

import pprint
from _ctypes import Union

import psychopy
import psychopy.gui
import xlrd
import csv
from psychopy import core, visual, data, event, logging, clock
import random
import time as clock
import pygame
from psychopy.gui import Dlg
import psychopy.tools.filetools
import os
import sys
import datetime
import numpy as np
from numpy.random import random, randint, normal, shuffle
from psychopy.visual import ImageStim

#shutdown key

event.globalKeys.add(key='q', func=core.quit, name='shutdown')

# upload excel reward structure

#datafile = xlrd.open_workbook(r "C:\Users\ic18563\OneDrive - University of Bristol\python different\python start\sensitivity_reward_condition.xlsx")
#workbook = xlrd.open_workbook(datafile)

#datafile= xlrd.open_workbook (r "C:\Users\ic18563\OneDrive - University of Bristol\python different\python start\sensitivity_punishment_condition.xlsx")
#workbook = xlrd.open_workbook(datafile)

# Participant info for everybody

gui = psychopy.gui.Dlg()
gui.addField("Participant Number:", "Ilaria")
gui.addField("Condition Number:", 1)
gui.addField("Age:", 22)
gui.addField("Gender(m/f/o):", "f")
gui.show()

participant_num = (gui.data[0])
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
screen_size = [1000, 1000]
gratings_h_size = [200, 200]
gratings_v_size = [200, 200]
fixationcross_size = [50, 50]

# Setup the Window

win = psychopy.visual.Window(
    units='pix',
    size=screen_size,
    fullscr=False, # change in True when you run the actual experiment and change the screen size into the actual size of the screen of the pc you will use
    color=[0, 0, 0])

print('setting win...')

print('loading images...')
pos1 = [200, -200]
pos2 = [-200, -200]
rectangle_right = psychopy.visual.Rect(win=win, units="pix", width=gratings_h_size[0] + 10, height=gratings_h_size[1] + 10,lineColor='green', colorSpace='rgb', pos=pos1)
rectangle_left = psychopy.visual.Rect(win=win, units="pix", width=gratings_v_size[0] + 10, height=gratings_v_size[1] + 10,lineColor='green', colorSpace='rgb', pos=pos2)
gratings_h = psychopy.visual.ImageStim(win=win, image="gratings_h.png", color=(1.0, 1.0, 1.0), size=gratings_h_size, units='pix', pos=pos1)
gratings_v = psychopy.visual.ImageStim(win=win, image="gratings_v.png", color=(1.0, 1.0, 1.0), size=gratings_v_size, units='pix', pos=pos2)
fixation_cross = psychopy.visual.ImageStim(win=win, image="fixation_cross.png", color=(1.0, 1.0, 1.0), size=fixationcross_size, units='pix', pos=[0, 200])

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

instruction_list = {"earn money": 'INSTRUCTIONS_REWARD_CONTR', "not lose": 'INSTRUCTIONS_PUNISHMENT_CONTR'}

def get_instructions (instruction_list):
        result = (instruction_list)
        print(result[0], [1])
        return result[0], result[1]

def get_starting_screen_control (starting_screen_list):
        result = (starting_screen_list)
        print(result[0], [1])
        return result[0], result[1]


#starting_screen_list = {"text_rule_FixationCross": '+', "arms": ('toy1','toy2')}
starting_screen_list = {"text_rule_FixationCross": ('fixation_cross'), "arms": ('gratings_h','gratings_v')}

# instructions control block of reward condition (earn money)
INSTRUCTIONS_REWARD_CONTR = """INSTRUCTIONS:
    Over the fixation point will be presented an amount of money.In this condition you will start with a  
    debit condition (-1£). Your task is to extinct your debit and when possible earn one pound by using one of the two
    arms (squares) available at the side of the screen.
    One of the two is more successful and it is more likely that will make you extinct the debit or earn money.
    The other one might make you remain in the debit condition. 
    Use left and right arrows to select the arm you think is more successful. 
    Pay attention, the good arm may change!

    Good luck!

    Press 'space' bar to begin.
    """

# instructions control block of punishment condition (not lose money)
INSTRUCTIONS_PUNISHMENT_CONTR = """INSTRUCTIONS:
    Over the fixation point will be presented an amount of money. In this condition you will start with zero money (0£). 
    Your task is to earn the pound as many time as possible with one of the 2 arms (squares) available. 
    One of the two is more successful and it will make earn money, 
    the other one might make stay without money or make you loose (-1£). 
    Use left and right arrow to select the arm you think is successful. 
    Pay attention, the good arm may change!

    Good luck!

    Press 'space' bar to begin.
    """


def bandit_task_control (selected_value, arms, stimuli, feedback, window):
    # define instructions
    # print(messages:["welcome"],["break"],["thanks"])
    print('selected_value is %d' % selected_value)
    instruction_result_text = ""
    if selected_value == 1:
        instruction_result_text, is_reward = get_instructions ([INSTRUCTIONS_REWARD_CONTR, True])

    if selected_value == 2:
        instruction_result_text, is_reward = get_instructions ([INSTRUCTIONS_PUNISHMENT_CONTR, True])

    elif selected_value < 1 or selected_value > 2:
        sys.exit("Unknown condition number")

    print('instruction_result is %s and is_reward=%s' % (instruction_result_text, is_reward))

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

# starting screen
    # screen experiments
    print('starting screen is %d' % selected_value)
    starting_screen_control = ""
    if selected_value > 0:
        starting_screen, is_reward = get_starting_screen_control (([fixation_cross, True],[arms, True]))
        print('display fixation cross and arms')
        while clock.getTime() < 1000:
            gratings_h.draw()
            gratings_v.draw()
            fixation_cross.draw()


def control_trial(is_reward, s=None):
    print("start control with is_reward=%s..." % s)
    return 0



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

is_reward = bandit_task_control (cond_num, None, None, None, win)

exit(0)



# dictionary of welcome, break and thanks across conditions
messages = {
    "welcome": "Welcome to our study. Thanks for taking part to this experiment! Press the'SPACE' bar to continue",
    "break": "The first part has been completed! Take some time to rest and press the'SPACE' bar when you are ready to proceed.",
    "thanks": "Congratulations, you have completed the experiment! Thank you for your participation! For any further question, do not hesitate to contact the reseachers."}
if is_reward is False or is_reward is True and is_exp is True or is_exp is False:
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

# Pause for a break every 100 trials

#if trials.thisN % 100 != 0: # this isn't trial number 100, 200, 300...
#    continueRoutine = False
#    return ("break")# so don't run the pause routine this time.

#take_a_break = "The first part has been completed! Take some time to rest and press the'SPACE' bar when you are ready to proceed." #take a break screen
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
#if trials.thisN % 200 != 0:
#        continueRoutine = False
#        return "thanks"
#thanks_message = "Congratulations, you have completed the experiment! Thank you for your participation! For any further question, do not hesitate to contact the reseachers." #thanks screen
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

# determine value of the keys
psychopy.event.waitKeys()

keys = psychopy.event.getKeys(
    keyList=["left", "right"],
    timeStamped=clock
)

for key in keys:

    if key[0] == "left":
        key_num = 1
    else:
        key_num = 0

    responses.append([key_num, key[1]])

data = []

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
dataFile.write('Participant_num, cond_num, is_exp, trial, choice, ReactionTime, leftOutcome, rightoutcome, leftProbability, rightProbability, correct\n')  # add info you want to store
dataFile.write("%i, %i, %s, %i, %i, %i, %i, %i, %i, %i, %i" % ())

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


# arms settings control condition

trialClock = core.Clock()


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



# define function for the task


# cleaning up, closing the window and experiment

win.close()
core.quit()


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
win.flip()
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


# psychopy.event.waitKeys()
# clock = psychopy.core.Clock()
# keys = psychopy.event.waitKeys(keyList=["left", "right"])
# keys = psychopy.event.waitKeys(timeStamped=clock)

# print(keys)

# win.close()


# link to xlsx file
#position []
#answer=xlrd.open_workbook(r'answer_contr.xlsx')
#sheet=answer.sheet_by_index(0)

# save data in excel with labels

# Thanks screen common across conditions

text_rule_thanks= """
Congratulations, you have completed the experiment! Thank you for your participation! For any further question, do not hesitate to contact the reseachers.
 """
text_stim_screen=psychopy.visual.TextStim(
win=win,
text=text_rule_thanks,
color=(-1,-1,-1), height=30.0)

# cleaning up, closing the window and experiment

# win.close()
# core.quit()


def main():
    print("python main function")


if __name__ == '__main__':
    main()

