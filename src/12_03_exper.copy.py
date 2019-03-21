# 07/03/2019 definitive version

# Author: Ilaria Costantini

import psychopy
import psychopy.gui
import xlrd
import random
from psychopy import core, visual, data, event, logging, clock
import os
import pandas as pd
#logging.console.setLevel(logging.DEBUG)
import time
import numpy as np


NUMBER_OF_ITERATION = 10

reaction_times= []
leftoutcomes= []
rightoutcomes= []
pressed_lefts= []
pos_right = [200, -200]
pos_left = [-200, -200]

rt = clock.getTime()
# take reaction times

def load_conditions():
    """
    load conditions
    """

    file_paths = { 'reward': r'C:\Users\ic18563\OneDrive - University of Bristol\python different\python start\Experimental - Copy\sensitivity_reward_condition_exc.xlsx',
                   'punishment': r'C:\Users\ic18563\OneDrive - University of Bristol\python different\python start\Experimental - Copy\sensitivity_punishment_condition_exc.xlsx'
                 }
    psychopy.logging.debug('upload conditions....')
    dataFile_reward = pd.read_excel(file_path['reward'])
    dataFile_punishment= pd.read_excel(file_path['punishment'])
    
    
    psychopy.logging.debug('conditions uploaded....')
    
    psychopy.logging.debug('define which column to use for what...')
    
    #need to convert pandas dataframe to python list after append.
    df = pd.ExcelFile(file_path['reward']).parse('sensitivity_reward') 
    right_outcome_reward=[]
    right_outcome_reward.append(df['right_outcome'])
    right_outcome_reward = right_outcome_reward[0].values.tolist()
    
    df = pd.ExcelFile(file_path['reward']).parse('sensitivity_reward') 
    left_outcome_reward=[]
    left_outcome_reward.append(df['left_outcome'])
    left_outcome_reward = left_outcome_reward[0].values.tolist()
    
    df = pd.ExcelFile(file_path['punishment']).parse('sensitivity_punishment')
    right_outcome_punish=[]
    right_outcome_punish.append(df['right_outcome'])
    right_outcome_punish = right_outcome_punish[0].values.tolist()
    
    df = pd.ExcelFile(file_path['punishment']).parse('sensitivity_punishment')
    left_outcome_punish=[]
    left_outcome_punish.append(df['left_outcome'])
    left_outcome_punish = left_outcome_punish[0].values.tolist()
    
    psychopy.logging.debug('column defined!', right_outcome_reward, left_outcome_reward)
    return right_outcome_reward, left_outcome_reward, right_outcome_punish, left_outcome_punish

# define welcome,break, thanks, equal across conditions
WELCOME = """
        Welcome to our study. Thanks for taking part to this experiment! Press the'SPACE' bar to continue
        """
BREAK = """
        Take a break before continuing. Press the 'SPACE' bar to continue
        """
THANKS = """
        Congratulations! you have completed this session!
        Thanks for your contribution!!!
        call the experimenter now :) 
        """
# instructions experimental block of reward condition (soothe the baby)
INSTRUCTIONS_REWARD_EXP = """
        Over the fixation point a distressed baby face will be presented, 
        your task is to soothe the baby, by choosing  one of the 2 toys available. 
        One of the two toys is more likely to work  and stop the baby crying or even make the baby smile! 
        the other toy will not produce any change.
        use left and right arrow to select the toy you think is better and try to soothe the baby as much as possible!
        Pay attention, the good toy may change!
        Good luck!
        Press 'space' to begin.
        """

# instructions experimental block of punishment condition (excite the baby)
INSTRUCTIONS_PUNISHMENT_EXP = """
    Over the fixation point a neutral baby face will be presented, 
    your task is to make the baby happy with one of the 2 toys available. 
    One of the two is more successful and it will make the baby smile! 
    the other might have no effect or may even distress the baby!
    use left and right arrow to select the toy you think is better and try to make the baby smile as much as possible!
    Pay attention, the good toy may change!
    Good luck!
    Press 'space' bar to begin.
    """

def init_elements_in_window():
    window = init_window()
    pos_right = [200, -200]
    pos_left = [-200, -200]
    toy_size = [200, 200]
    face_size = [150, 200]
    fixationcross_size = [200, 200]
    rectangle_right = psychopy.visual.Rect(win=window, units="pix", width=toy_size[0] + 10, height=toy_size[1] + 10,
                                        lineColor='green', colorSpace='rgb', pos=pos_right)
    rectangle_left = psychopy.visual.Rect(win=window, units="pix", width=toy_size[0] + 10, height=toy_size[1] + 10,
                                        lineColor='green', colorSpace='rgb', pos=pos_left)
    toy_bear = psychopy.visual.ImageStim(win=window, image="teddy_bear.png", color=(1.0, 1.0, 1.0), size=toy_size,   #colored images
                                        units='pix',
                                        pos=pos_right)
    toy_duck = psychopy.visual.ImageStim(win=window, image="duck_1.png", color=(1.0, 1.0, 1.0), size=toy_size,   #colored images!
                                        units='pix',
                                        pos=pos_left)
    happyface = psychopy.visual.ImageStim(win=window, image="babyhappy2.png", color=(1.0, 1.0, 1.0),
                                        size=face_size,
                                        units='pix', pos=[0, 150])
    neutralface = psychopy.visual.ImageStim(win=window, image="babyneutral2.png", color=(1.0, 1.0, 1.0),
                                        size=face_size,
                                        units='pix', pos=[0, 150])
    sadface = psychopy.visual.ImageStim(win=window, image="babyneg2.png", color=(1.0, 1.0, 1.0), size=face_size,
                                        units='pix', pos=[0, 150])
    fixation_cross = psychopy.visual.ImageStim(win=window, image="fix_cros.png", color=(1.0, 1.0, 1.0),
                                        size=fixationcross_size, units='pix', pos=[0, 150])

    right_highlight = psychopy.visual.Rect(win=window, pos=pos_right, width=250, height=250, color=(0.0, 1.0, 0.0),
                                        units='pix')

    left_highlight = psychopy.visual.Rect(win=window, pos=pos_left, width=250, height=250, color=(0.0, 1.0, 0.0),
                                        units='pix')

    return window, rectangle_right, rectangle_left, toy_bear, toy_duck, happyface, neutralface, sadface, fixation_cross, right_highlight, left_highlight

def init_window():
    screen_size = [1000, 1000]
    window = psychopy.visual.Window(
        units='pix',
        size=screen_size,
        fullscr=False,
        # change in True when you run the actual experiment and change the screen size into the actual size of the screen of the pc you will use
        color=[0, 0, 0])
    return window

def show_dialog_and_get_info():
    print("show_dialog...")
    gui = psychopy.gui.Dlg()
    gui.addField("Participant Number:", "001")
    gui.addField("Condition Number:", 1)
    gui.addField("Age:", 26)
    gui.addField("Gender(m/f/o):", "f")
    # this is a blocking function. as long as the participant has not clicked ok the code progression
    # will be blocked here
    gui.show()
    participant_number = int(gui.data[0])
    cond_num = int(gui.data[1])
    age = int(gui.data[2])
    gender = (gui.data[3])
    return participant_number, cond_num, age, gender

def show_messages_and_wait(window, cpt):
    messages = {'welcome': WELCOME,
                'break' : BREAK,
                'thanks': THANKS}
    this_message = {1: 'welcome', 5: 'break', 10: 'thanks'}
    try: 
        text = messages[this_message[cpt]]
    except KeyError:
        return 
    text_stim = psychopy.visual.TextStim(
        win=window,
        text= text,
        color=(-1, -1, -1), height=30.0)
    text_stim.draw(window)
    window.flip()
    psychopy.event.waitKeys(keyList=['space'])
    print("user pressed space -> go to next step !")
    return is_reward

def show_instructions_and_wait (window, is_reward, cpt):
    print("is_reward=%s" % is_reward)
    if cpt<2:
        if is_reward is True:
            print ("true")
            instructions_text = INSTRUCTIONS_REWARD_EXP
        elif is_reward is False:
            print("false")
            instructions_text = INSTRUCTIONS_PUNISHMENT_EXP
        print(instructions_text)
        text_stim = psychopy.visual.TextStim(
            win=window,
            text= instructions_text,
            color=(-1, -1, -1), height=30.0)
        text_stim.draw(window)
        window.flip()
        psychopy.event.waitKeys(keyList=['space'])
        print("user pressed space -> go to next step !")
        return is_reward
    else:
        window.flip()

def is_even (window, participant_number):
    print('setting if part_num is odd or even')
    if (participant_number % 2) == 0:
        is_even = True
        print("{0} is Even".format(participant_number))
    else:
        is_even = False
        print("{0} is Odd".format(participant_number))
    print("is_even=%s" % is_even)
    return is_even

def position_arms (window, is_even, toy_bear, toy_duck, pos_left, pos_right):
    print('setting position of arms if part_num is odd or even')
    if is_even is True:
        print("it is even")
        toy_bear.pos = pos_right
        toy_duck.pos = pos_left
    elif is_even is False:
        print("it is odd")
        print(toy_bear.pos, toy_duck.pos)
        toy_bear.pos = pos_left
        toy_duck.pos = pos_right
        print(toy_bear.pos, toy_duck.pos)
        
    window.flip()
    return is_even

def experiment_trial(is_reward, is_even, position_arms, window, right_highlight, left_highlight, toy_bear, toy_duck, happy_face, neutral_face, sad_face):
    print("start experiment trial with is_reward=%s..." % is_reward)
    fixation_cross.draw(window)
    window.flip()
    core.wait(0.5)
    print("waited 500 ms.")
    fixation_cross.draw(window)
    window.flip()
    core.wait(0.5)
    print("waited 500 ms.")
    # remove fixation cross
    window.flip()
    if is_reward is True:
        sad_face.draw(window)

    elif is_reward is False:
        neutral_face.draw(window)

    toy_bear.draw(window)
    toy_duck.draw(window)

    window.flip()
    start = time.time()
    response = psychopy.event.waitKeys(keyList=['left', 'right','escape'])
    end = time.time()
    reaction_time = end - start
    print(reaction_time)
    reaction_times.append(reaction_time)

    print(response)
    # highlight selected items
    pressed_left = None
    
    if 'left' in response:
        pressed_left = True
        left_highlight.draw(window)
        toy_duck.draw(window)
        toy_bear.draw(window)
    if 'right' in response:
        pressed_left = False
        right_highlight.draw(window)
        toy_bear.draw(window)
        toy_duck.draw(window)
        window.flip()
    if 'escape' in response:
        window.close()
        core.quit()

    feedback (is_reward, is_even, window, right_highlight, left_highlight, toy_bear, toy_duck, happy_face, neutral_face, sad_face, pressed_left)

    pressed_lefts.append(pressed_left)

def process_result_and_wait(is_reward, is_even, window, happy_face, neutral_face, sad_face, pressed_left, left_highlight, right_highlight, toy_bear, toy_duck):
    #redraw previous state
    if pressed_left:
        left_highlight.draw(window)
        toy_bear.draw(window)
        toy_duck.draw(window)
    else:
        right_highlight.draw(window)
        toy_bear.draw(window)
        toy_duck.draw(window)

#decide which baby face to display
def feedback (is_reward, is_even, window, right_highlight, left_highlight, toy_bear, toy_duck, happy_face, neutral_face, sad_face, pressed_left):
    print('feedback...')
    rnd_right_outcome_reward =  random.choice(right_outcome_reward)
    rnd_left_outcome_reward =  random.choice(left_outcome_reward)
    rnd_right_outcome_punish =  random.choice(right_outcome_punish)
    rnd_left_outcome_punish =  random.choice(left_outcome_punish)

    status = () 
#    status = None
    if is_reward is True: 
        if pressed_left:
            print('is_reward=%s'%is_reward)
            print('pressed_left')
            feedback = rnd_left_outcome_reward
            left_outcome_reward.append(str(status))
            right_outcome_reward.append('')
        else:
            print('is_reward=%s'%is_reward)
            print('pressed_right')
            feedback = rnd_right_outcome_reward
            right_outcome_reward.append(str(status))
            left_outcome_reward.append('')
        
        print('feedback')
        print(feedback)
        
        if feedback == 1:
            core.wait(0.5)
            happy_face.draw(window)
            status = 1
        if feedback == 0:
            core.wait(0.5)
            neutral_face.draw(window)
            status = 0
        if feedback == -1:
            core.wait(0.5)
            sad_face.draw(window)
            status = -1
        toy_bear.draw(window)
        toy_duck.draw(window)
        window.flip()

    elif is_reward is False:
        if pressed_left:
            print('is_reward=%s'%is_reward)
            print('pressed_left')
            feedback = rnd_left_outcome_punish
            left_outcome_punish.append(str(status))
            right_outcome_punish.append('')
        else:
            print('is_reward=%s'%is_reward)
            print('pressed_right')
            feedback = rnd_right_outcome_punish
            right_outcome_punish.append(str(status))
            left_outcome_punish.append('')

        if feedback == 1:
            core.wait(0.5)
            happy_face.draw(window)
            status = 1
        if feedback == 0:
            core.wait(0.5)
            neutral_face.draw(window)
            status = 0
        if feedback == -1:
            core.wait(0.5)
            sad_face.draw(window)
            status = -1
        toy_bear.draw(window)
        toy_duck.draw(window)
        window.flip()

    feedback.append(int(feedback))

    core.wait(1)


if __name__ == "__main__":
    print("start experiment...")
    participant_number, cond_num, age, gender = show_dialog_and_get_info()
    print("participant name is %s, cond_num is %d, age is %d, gender is %s."
          %(participant_number, cond_num, age, gender))
    if cond_num == 1:
        is_reward = True
    elif cond_num == 2:
        is_reward = False
    window, rectangle_right, rectangle_left, toy_bear, toy_duck, happy_face, neutral_face, sad_face, fixation_cross, right_highlight, left_highlight = init_elements_in_window()
    
    position_arms (window, is_even(window, participant_number), toy_bear, toy_duck, pos_left, pos_right)
    
    print("windows elements are ready for use.")

    (right_outcome_reward, left_outcome_reward, right_outcome_punish, left_outcome_punish) = load_conditions()

    cpt_iteration = 1
    while True:
        print("before show message")
        show_messages_and_wait(window, cpt_iteration)
        show_instructions_and_wait(window, is_reward, cpt_iteration)
        if cpt_iteration == 10:
           break 
        experiment_trial(is_reward, is_even, position_arms, window, right_highlight, left_highlight, toy_bear, toy_duck, happy_face, neutral_face, sad_face)
        cpt_iteration += 1
        print("%d experiment trials has been performed." % cpt_iteration)



    # Store info about the experiment session
    expName = 'bandit_exp'
    expInfo = {}
    expInfo['gui'] = {'participant_number': participant_number, 'cond_num': cond_num, 'age': age, 'gender': gender}
    expInfo['date'] = data.getDateStr()  # add a simple timestamp
    expInfo['expName'] = expName

    # store frame rate of monitor if we can measure it
    expInfo['frameRate'] = window.getActualFrameRate()
    if expInfo['frameRate'] != None:
        frameDur = 1.0 / round(expInfo['frameRate'])
    else:
        frameDur = 1.0 / 60.0  # could not measure, so guess

    print("expInfo", expInfo)

    # Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
    _thisDir = os.curdir
    psychopy.logging.debug(expInfo)

    a = expInfo['gui']['participant_number']
    b = expInfo['expName']
    c = expInfo['date']

    print(a,b,c)


    filename = '%d_%s_%s.csv' % (a, b, c)
    psychopy.logging.debug('filename= %s' %filename)

    #with open(filename, 'a') as file:
    #        file.write('participant_num, cond_num, cpt_iteration, reaction_times, leftoutcomes, rightoutcomes, pressed_lefts\n')
    #        for i in range(0, cpt_iteration):
    #            file.write('%d,%d,%d,%.4f,%s,%s,%s\n'%(participant_number, cond_num, i, reaction_times[i], leftoutcomes[i], rightoutcomes[i], pressed_lefts[i]))
  #  with open(filename, 'a') as file:
  #          file.write('participant_num, cond_num, cpt_iteration, reaction_times, left_outcome_reward, right_outcome_reward, left_outcome_punish, right_outcome_punish, pressed_left\n')
  #          for i in range(0, len(reaction_times)):
  #              file.write('%d,%d,%d,%.4f,%s,%s,%s,%s,%s\n'%(participant_number, cond_num, i, reaction_times[i], left_outcome_reward[i],  right_outcome_reward[i], left_outcome_punish[i], right_outcome_punish[i], pressed_lefts[i]))
    with open(filename, 'a') as file:
            file.write('participant_num, cond_num, cpt_iteration, reaction_times,feedback, pressed_left\n')
            for i in range(0, len(reaction_times)):
                file.write('%d,%d,%d,%.4f,%d,%s\n'%(participant_number, cond_num, i, reaction_times[i], feedback[i], pressed_lefts[i]))

    # determine when a key is pressed
    clock = psychopy.core.Clock()
    keys = psychopy.event.waitKeys(timeStamped=clock)
    print (keys)
    window.flip()

    # Create some handy timers
    globalClock = core.Clock()  # to track the time since experiment started
    routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine 

    # keep track of the time
    print('track time...')
    globalClock = core.Clock()
    trialClock = core.Clock()

core.quit()
core.close()
