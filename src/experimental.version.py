# Multi-armed bandit task, experimental condition. We use infant stimuli as images and toys as arms.
# Author: Ilaria Costantini
# Last version: 27/02/2019


# coding=utf-8
from __future__ import absolute_import, division

import pprint
from _ctypes import Union

import psychopy
import psychopy.gui
import xlrd
import csv
from psychopy import core, visual, data, event, logging, clock, monitors
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


"""
SET VARIABLES
"""
# Monitor parameters
MON_DISTANCE = 60 # Distance between subject's eyes and monitor
MON_WIDTH = 50 # Width of your monitor in cm
MON_SIZE = [1024, 768] # Pixel dimensions of your monito
SAVE_FOLDER = 'data' # Log is saved to this folder. The folder is created if it doesn't exist

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

#fileName = V['condition_num'] +V['participant_num']+'['+ time.strftime('%Y%m%d-%H%M', time.localtime())+').tsv'




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
fixationcross_size = [70, 70]

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
rectangle_right = psychopy.visual.Rect(win=win, units="pix", width=toy1_size[0] + 10, height=toy1_size[1] + 10,lineColor='green', colorSpace='rgb', pos=pos1)
rectangle_left = psychopy.visual.Rect(win=win, units="pix", width=toy2_size[0] + 10, height=toy2_size[1] + 10,lineColor='green', colorSpace='rgb', pos=pos2)
toy1 = psychopy.visual.ImageStim(win=win, image="toy1_bear.png", color=(1.0, 1.0, 1.0), size=toy1_size, units='pix', pos=pos1)  # type: ImageStim
toy2 = psychopy.visual.ImageStim(win=win, image="toy2_duck.png", color=(1.0, 1.0, 1.0), size=toy2_size, units='pix', pos=pos2)
happyface = psychopy.visual.ImageStim(win=win, image="babyhappy2.png", color=(1.0, 1.0, 1.0), size=facehappy_size, units='pix', pos=[0, 200])
neutralface = psychopy.visual.ImageStim(win=win, image="babyneutral2.png", color=(1.0, 1.0, 1.0), size=faceneutral_size, units='pix', pos=[0, 200])
sadface = psychopy.visual.ImageStim(win=win, image="babyneg2.png", color=(1.0, 1.0, 1.0), size=facesad_size, units='pix', pos=[0, 200])
fixation_cross = psychopy.visual.ImageStim(win=win, image="fixation_cross.png", color=(-1.0, -1.0, -1.0), size=fixationcross_size, units='pix', pos=[0, 200])

#text_rule_FixationCross = "+"
#text_stim_screen = psychopy.visual.TextStim(
#    win=win,
#    text=text_rule_FixationCross,
#    color=(-1, -1, -1), pos=[0, 200])
#win.flip()

#fixation_cross = visual.GratingStim(win, color=-1, colorSpace='rgb',
#                              tex=None, mask='circle', size=0.2)


# fixation cross
fixation_cross = visual.ShapeStim(win, 
    vertices=((0, -2.5), (0, 2.5), (0,0), (-2.5,0), (2.5, 0)),
    lineWidth=20,
    closeShape=False,
    lineColor="black"
)
#fixation_cross.draw()
#core.wait(1000)
#win.flip()

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



def get_instructions (instruction_list):
        result = (instruction_list)
        print(result[0], [1])
        return result[0], result[1]

instruction_list = {"soothe the baby": 'INSTRUCTIONS_REWARD_EXP', "excite the baby": 'INSTRUCTIONS_PUNISHMENT_EXP'}


def get_starting_screen_experimental (starting_screen_list):
        result = (starting_screen_list)
        print(result[0], [1])
        return result[0], result[1]

starting_screen_list = {"fixation_cross": ('fixation_cross'), "arms": ('toy1','toy2')}


def get_baseline_screen_expt_reward (baseline_screen_rew_list):
        result = (baseline_screen_rew_list)
        print(result[0],[1])
        return result[0], result[1]

baseline_screen_rew_list = {"sadface": ('sadface'), "arms": ('toy1','toy2')}

def get_baseline_screen_expt_punishment (baseline_screen_pun_list):
        result = (baseline_screen_pun_list)
        print(result[0],[1])
        return result[0], result[1]

baseline_screen_pun_list = {"neuface": ('neutralface'), "arms": ('toy1','toy2')}

# messages 
# instructions experimental block of reward condition (earn money)
INSTRUCTIONS_REWARD_EXP = """INSTRUCTIONS:
    Over the fixation point will be presented a distressed baby face, 
    your task is to soothe the baby with one of the 2 toys available. 
    One of the two is more successful and it will make the baby stop crying (neutral face) or being happy! 
    The other one will not produce any change.
    Use left and right arrows to select the toy you think is better and try to soothe the baby as much as possible!
    Pay attention, the good toy may change!

    Good luck!

    Press 'space' to begin.
    """

# instructions experimental block of punishment condition (excite the baby)
INSTRUCTIONS_PUNISHMENT_EXP = """INSTRUCTIONS:
    Over the fixation point will be presented a neutral baby face, 
    your task is to make the baby happy with one of the 2 toys available. 
    One of the two is more successful and it will make the baby being happy! 
    The other might have no effect or even distress the baby!
    Use left and right arrows to select the toy you think is better and try to make the baby as much as possible!
    Pay attention, the good toy may change!

    Good luck!

    Press 'space' bar to begin.
    """

# setting
payoffMean = ['payoffMean']
#rounds 
rounds = range (['round'])

# Payoffs 
payofftoy1 = [random.gauss(payoffMean, payoffSD) for i in rounds] # BOX_1 the gain sequence 
if V['cond_num'] == '1':
    payofftoy1 = [random.gauss(payoffMean+14, payoffSD) for i in rounds[0:30]]
    payofftoy1 += [random.gauss(payoffMean-14, payoffSD) for i in rounds[30:45]]
    payofftoy1 += [random.gauss(payoffMean+14, payoffSD) for i in rounds[45:63]]
    payofftoy1 += [random.gauss(payoffMean+7, payoffSD) for i in rounds[63:86]]
    payofftoy1 += [random.gauss(payoffMean-14, payoffSD) for i in rounds[86:100]]
    payofftoy1 += [random.gauss(payoffMean-7, payoffSD) for i in rounds[100:125]]
    payofftoy1 += [random.gauss(payoffMean+7, payoffSD) for i in rounds[125:140]]
    payofftoy1 += [random.gauss(payoffMean-7, payoffSD) for i in rounds[140:162]]
    payofftoy1 += [random.gauss(payoffMean+7, payoffSD) for i in rounds[162:len(rounds)]]
elif ['cond_num'] == '2':
    payofftoy2 = [random.gauss(payoffMean-14, payoffSD) for i in rounds[0:30]]
    payofftoy2 += [random.gauss(payoffMean+14, payoffSD) for i in rounds[30:45]]
    payofftoy2 += [random.gauss(payoffMean-14, payoffSD) for i in rounds[45:63]]
    payofftoy2 += [random.gauss(payoffMean-7, payoffSD) for i in rounds[63:86]]
    payofftoy2 += [random.gauss(payoffMean+14, payoffSD) for i in rounds[86:100]]
    payofftoy2 += [random.gauss(payoffMean+7, payoffSD) for i in rounds[100:125]]
    payofftoy2 += [random.gauss(payoffMean-7, payoffSD) for i in rounds[125:140]]
    payofftoy2 += [random.gauss(payoffMean+7, payoffSD) for i in rounds[140:162]]
    payofftoy2 += [random.gauss(payoffMean-7, payoffSD) for i in rounds[162:len(rounds)]]
else:
    payofftoy2 = [0 for i in rounds] # to check


# Stimuli positions
if ['cond_num'] == '1' or ['cond_num'] == '2':
    # successful is LEFT and unsuccessful is RIGHT
    toy1 = psychopy.visual.ImageStim(win=win, image="toy1_bear.png", color=(1.0, 1.0, 1.0), size=toy1_size, units='pix', pos=pos1)  # type: ImageStim
    toy2 = psychopy.visual.ImageStim(win=win, image="toy2_duck.png", color=(1.0, 1.0, 1.0), size=toy2_size, units='pix', pos=pos2)


# the correct answer

if ['cond_num'] == '1' or ['cond-num'] == '2':
    correctAns = ['right' for i in rounds[0:30]]
    correctAns += ['left' for i in rounds[30:45]]
    correctAns += ['right' for i in rounds[45:63]]
    correctAns += ['right' for i in rounds[63:86]]
    correctAns += ['left' for i in rounds[86:100]]
    correctAns += ['left' for i in rounds[100:125]]
    correctAns += ['right' for i in rounds[125:140]]
    correctAns += ['left' for i in rounds[140:162]]
    correctAns += ['right' for i in rounds[162:len(rounds)]]

def feedback(trial):
    """
    we will give feedback to participants
    """
    # extract gain from participant's selection 

    if trial['response'] == 'left':
        choice = u'left'
        if ['cond_num'] in {'1', '2'}:
            payoff = trial['payoffsucc']
        else:
            payoff = trial['payoffunsucc']
    else:
        choice = u'right'
        if ['cond_num'] in {'1', '2'}:
            payoff = trial['payoffsucc']
        else:
            payoff = trial['payoffunsucc']


# the correct answer
if ['cond_num'] == '1':
    correctAns = ['right' for i in rounds[0:30]]
    correctAns += ['left' for i in rounds[30:45]]
    correctAns += ['right' for i in rounds[45:63]]
    correctAns += ['right' for i in rounds[63:86]]
    correctAns += ['left' for i in rounds[86:100]]
    correctAns += ['left' for i in rounds[100:125]]
    correctAns += ['right' for i in rounds[125:140]]
    correctAns += ['left' for i in rounds[140:162]]
    correctAns += ['right' for i in rounds[162:len(rounds)]]
elif ['condi_num'] == '2':
    correctAns = ['left' for i in rounds[0:30]]
    correctAns += ['right' for i in rounds[30:45]]
    correctAns += ['left' for i in rounds[45:63]]
    correctAns += ['left' for i in rounds[63:86]]
    correctAns += ['right' for i in rounds[86:100]]
    correctAns += ['right' for i in rounds[100:125]]
    correctAns += ['left' for i in rounds[125:140]]
    correctAns += ['right' for i in rounds[140:162]]
    correctAns += ['left' for i in rounds[162:len(rounds)]]
 

#starting_screen_experimental

def bandit_task_experimental (selected_value, arms, stimuli, feedback, window):
    # define instructions
    # print(messages:["welcome"],["break"],["thanks"])
    print('selected_value is %d' % selected_value)
    instruction_result_text = ""
    if selected_value == 1:
        instruction_result_text, is_reward = get_instructions ([INSTRUCTIONS_REWARD_EXP, True])

    if selected_value == 2:
        instruction_result_text, is_reward = get_instructions ([INSTRUCTIONS_PUNISHMENT_EXP, True])

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


# screen experiments

    print('selected_value is %d' % selected_value)
    starting_screen_experimental = ""
    if selected_value > 0:
        starting_screen = get_starting_screen_experimental (([fixation_cross, True],[arms, True]))
        print('display fixation cross and arms')
        core.wait(0.5)
    print ('starting_screen_experimental is %s' % (starting_screen_experimental))


    baseline_screen = ""
    if selected_value == 1 and clock.getTime() > 0.5:  # baseline screen experimental reward condition
        baseline_screen, is_reward = get_baseline_screen_expt_reward (([sadface, True],[arms, True]))
        print(get_baseline_screen_expt_reward)

    if selected_value == 2 and clock.getTime() > 0.5:  # baseline screen experimental punishment condition 
        baseline_screen, is_reward = get_baseline_screen_expt_punishment (([neuface, True], [arms, True]))
        print(get_baseline_screen_expt_punishment)

    print ('baseline_screen is %s and is_reward=%s' % (baseline_screen, is_reward))


    while True:
        print('in while...')
        response = psychopy.event.waitKeys(keyList=['left', 'right'])
        print('after response')
        print(response)
        if 'left' in str(response):
            print("left!")
        elif 'right' in str(response):
            print("right!")
            break  # break out of the while-loop
                    
def experiment_trial(is_reward, s=None):
    print("start experiment trial with is_reward=%s..." % s)
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

is_reward = bandit_task_experimental (cond_num, None, None, None, win)

exit(0)

# Pause for a break every 100 trials

if trials.thisN % 50 != 0: # this isn't trial number 50, 100, 150, 200...
    continueRoutine = False
    #print("take_a_break")# so don't run the pause routine this time.

# define take a break, equal across conditions

print ('take a break')
take_a_break = "you are half way the first part! Take some time to rest and press the'SPACE' bar when you are ready to proceed."
text_stim_screen = psychopy.visual.TextStim(
    win=win,
    text=take_a_break,
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


# cleaning up, closing the window and experiment

win.close()
core.quit()


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


# psychopy.event.waitKeys()
# clock = psychopy.core.Clock()
# keys = psychopy.event.waitKeys(keyList=["left", "right"])
# keys = psychopy.event.waitKeys(timeStamped=clock)

# print(keys)

# win.close()

# link to xlsx file

#position []
#answer=xlrd.open_workbook(r'answer_exp.xlsx')
#sheet=answer.sheet_by_index(0)

# save data in excel with labels


# Thanks screen common across conditions
#if trials.thisN % 200 != 0:
  #     continueRoutine = False
  #  return "thanks"
print('thanks')
thanks= "Congratulations, you have completed the experimental session! Pass to the control session, ask the experimenter :)"
text_stim_screen=psychopy.visual.TextStim(
    win=win,
    text=thanks,
    color=(-1,-1,-1), height=30.0)
text_stim_screen.draw(win)
win.close()

# cleaning up, closing the window and experiment

# win.close()
# core.quit()


def main():
    print("python main function")


if __name__ == '__main__':
    main()
