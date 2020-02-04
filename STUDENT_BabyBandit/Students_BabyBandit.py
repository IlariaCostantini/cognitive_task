# 17/09/2019 Ilaria Costantini

# BabyBandit for Student
# Here a decision making task develped for women in pregnancy. You neeed to rate emotions and temperament of 3 baby faces before and after having completed the task
# press space every time to move forward
# For cocos participants the age range can vary from 13 to 55, in the case you need more flexibility because you have someone who is younger or older just change row number:
# Here you MUST add,  when starting inserting data in the initial square, in the row of the condition, the number 1, which stands for the "soothing" condition - the participant
# is interacting always with a baby who is crying and by choosing on eof the 2 toys has to try to stop the baby from being sad.
# EVERYTHING MUST BE IN THE SAME FOLDER, you need to have a folder named "Data cognitive task". Once the task has been completed, all the results will be automatically be saved in that
# folder.
# There is now a safe version then if you press esc is going to save anyway the data!

# I import few packages

import os
import random
import numpy
from numpy.random import normal
import sys
import pandas as pd
import psychopy
import psychopy.gui
from psychopy import core, visual, data, event, logging
import time
import xlsxwriter
import pip
import datetime


logging.console.setLevel(logging.DEBUG)

# Number of trials, now set at 200

TOTAL_NUMBER_OF_TRIALS = 200
OFFSET = 1

# setting few things which are costant
CONDITION_NUMBER = None
PARTICIPANT_NUMBER = None
reaction_times_experiment = []
initial_ratings = []
final_ratings = []
initial_ratings_temperament = []
final_ratings_temperament = []
feedbacks = []
pressed_lefts = []
pos_right = [200, -200]
pos_left = [-200, -200]
screen_size = [1000, 1000]
toy_size = [200, 200]
face_size = [150, 200]
fixation_cross_size = [200, 200]
initial_pos = [0, 150]


# loan the "reward structure" - I am actually loading an excel spreadsheet which contains the outcome they receive.
# If you chenge location, chenge the file_path as well

def load_conditions():
    """
    load conditions
    """
    print("system platform is = %s" % sys.platform)
    file_path = {
        'condition': r'condition.xlsx'
    }

    if sys.platform.startswith('macOS'):  # are these the right info?
        file_path = {
            'condition': r'O:\bandit_task\bandit_task\STUDENT_BabyBandit\condition.xlsx'}  # CHANGE FILE_PATH IF YOU CHANGE COMPUTER/LOCATION

    psychopy.logging.debug('upload conditions....')
    psychopy.logging.debug('conditions uploaded....')
    psychopy.logging.debug('define which column to use for what...')

    # need to convert pandas dataframe to python list after append.
    df = pd.ExcelFile(file_path['condition']).parse('sensitivity_outcomes')
    right_outcomes = [df['right_outcome']]
    right_outcomes = right_outcomes[0].values.tolist()

    df = pd.ExcelFile(file_path['condition']).parse('sensitivity_outcomes')
    left_outcomes = [df['left_outcome']]
    left_outcomes = left_outcomes[0].values.tolist()

    print("right_outcome_reward and left_outcome_reward")
    psychopy.logging.debug(right_outcomes)
    psychopy.logging.debug(left_outcomes)
    return right_outcomes, left_outcomes


# Text of various messages: welcome, instructions for rating and task in either version, thanks message and end.

WELCOME = "Welcome to our study.\n\nThanks for taking part to this experiment!" \
          "\nFirstly, you will be asked to rate the emotion and the temperament of some infant faces and then to proceed to the main experiment." \
          "\n\nPlease press the 'SPACE' bar to continue"
BREAK = "You are doing great,\n\nYou are in a paused mood.\nPress the 'SPACE' bar when you are ready to continue..."
THANKS = "Congratulations!!!\n\nyou have completed this session. Please take few seconds to rate the following images.\n\nYour contribution is really valuable to us!\n\n Press 'SPACE' to proceed."
CONGRATULATIONS = "Congratulations!!!\n\nYou completed the experiment.\nThanks for your participation! Call the experimenter."
# instructions experimental block of reward condition (soothe the baby)
INSTRUCTIONS_REWARD_EXP = "INSTRUCTIONS BANDIT TASK.\n\nOver the fixation point a distressed baby face will be presented, your task is to " \
                          "soothe the baby, by choosing one of the 2 toys available.\nOne of the two toys is more " \
                          "likely to work and stop the baby crying or even make the baby smile!" \
                          "\nUse the left and the right arrows of the keyboard to select the toy you think is better and" \
                          "\nTRY TO SOOTHE THE BABY AS MUCH AS POSSIBLE!\n\nPay attention, the good toy may change!\n\n" \
                          "Good luck! \n\nPress 'SPACE' to begin."

# instructions experimental block of punishment condition (excite the baby)
INSTRUCTIONS_PUNISHMENT_EXP = "INSTRUCTIONS BANDIT TASK.\n\nOver the fixation point a happy baby face will be presented, your task is to keep the " \
                              "baby happy with one of the 2 toys available.\nOne of the two is more successful and it " \
                              "will keep the baby smiling!" \
                              "\nUse the left and the right arrows of the keyboard " \
                              "to select the toy you think is better and \nTRY TO KEEP THE BABY HAPPY " \
                              "AS MUCH AS POSSIBLE!\n\n Pay attention, the good toy may change!" \
                              "\n\nGood luck!\n\nPress 'SPACE' bar to begin."


# what appears on the screen

def init_elements_in_window():
#    try:
        print('init_window start...')
        window = init_window()
        print('after')
        print(toy_size)
        print(pos_right)
        print(window)
        rectangle_right = psychopy.visual.Rect(win=window, units="pix", width=toy_size[0] + 10, height=toy_size[1] + 10,
                                               # change to white?
                                               lineColor='grey', pos=pos_right)
        print('after rect')
        print(rectangle_right == None)
        rectangle_left = psychopy.visual.Rect(win=window, units="pix", width=toy_size[0] + 10, height=toy_size[1] + 10,
                                              # change to white?
                                              lineColor='grey', pos=pos_left)
        toy_bear = psychopy.visual.ImageStim(win=window, image="toy1_bear.png", color=(1.0, 1.0, 1.0), size=toy_size,
                                             units='pix',
                                             pos=pos_right)
        toy_duck = psychopy.visual.ImageStim(win=window, image="toy2_duck.png", color=(1.0, 1.0, 1.0), size=toy_size,
                                             units='pix',
                                             pos=pos_left)
        happy_face = psychopy.visual.ImageStim(win=window, image="baby_happy.png", color=(1.0, 1.0, 1.0),
                                               size=face_size,
                                               units='pix', pos=initial_pos)
        neutral_face = psychopy.visual.ImageStim(win=window, image="baby_neutral.png", color=(1.0, 1.0, 1.0),
                                                 size=face_size,
                                                 units='pix', pos=initial_pos)

        sad_face = psychopy.visual.ImageStim(win=window, image="baby_sad.png", color=(1.0, 1.0, 1.0), size=face_size,
                                             units='pix', pos=initial_pos)
        fixation_cross = psychopy.visual.ImageStim(win=window, image="fix_cros.png", color=(1.0, 1.0, 1.0),
                                                   size=fixation_cross_size, units='pix', pos=[0, 150])
                                                   
        #right_highlight = psychopy.visual.Rect(win=window, pos=pos_right, width=250, height=250, color=(-0.5, -0.5, -0.5),
        #                                       # changed to dark grey!
        #                                       units='pix')
                                               
        right_highlight = psychopy.visual.ImageStim(win=window, image="dark_gray.png", pos=pos_right, units='pix')
                                               
        #left_highlight = psychopy.visual.Rect(win=window, pos=pos_left, width=250, height=250, color=(-0.5, -0.5, -0.5),
        #                                     # changed to dark grey!
        #                                     units='pix')
         
        left_highlight = psychopy.visual.ImageStim(win=window, image="dark_gray.png", pos=pos_left, units='pix')

        # remove time horizon
        #   rectangle_time = visual.Rect(win=window, name='rectangle_time', width=1000, height=50, ori=0,   #remove rectangle_time and rectangle_time_passing or make it of a neutral colour
        #                               pos=(0, -500),
        #                               lineWidth=3, lineColor=[-1, -1, -1], lineColorSpace='rgb', fillColor=[0, 0, 0],
        #                               fillColorSpace='rgb',
        #                               opacity=1, depth=0.0, interpolate=True)

        #   rectangle_time_passing = visual.Rect(win=window, name='rectangle_time_passing', width=0,
        #                                       height=50, ori=0, pos=(-500, -500), lineWidth=3,
        #                                       lineColor=[-1, -1, -1], lineColorSpace='rgb', fillColor=(0.0, 1.0, 0.0),
        #                                       fillColorSpace='rgb',
        #                                       opacity=1, depth=-1.0, interpolate=True)
        
        print(window == None)
        print(rectangle_left == None)
        print(rectangle_right == None)
        print(toy_bear == None)
        print(toy_duck == None)
        print(happy_face == None)
        print(neutral_face == None)
        print(sad_face == None)
        print(fixation_cross == None)
        print(right_highlight == None)
        print(left_highlight == None)
        
        
        return window, rectangle_right, rectangle_left, toy_bear, toy_duck, happy_face, neutral_face, sad_face, fixation_cross, right_highlight, left_highlight  # , rectangle_time, rectangle_time_passing
#    except Exception as e:
#        print('error while init_elements_in_window')
#        write_to_log_error_file('error in init_elements_in_window')
#        write_to_log_error_file(str(e))


def init_window():
    window = psychopy.visual.Window(
        units='pix',
        # winType='pygame',
        size=screen_size,
        fullscr=True,
        # CHANGE TO True when you run the actual experiment in order to have FULL sCREEN SIZE!!! --------IMPORTANT!!! -----------
        color=[0, 0, 0])
    return window


def init_and_show_gui():
    gui = psychopy.gui.Dlg()
    gui.addField("Participant Number:", )
    gui.addField("Condition Number:", )
    gui.addField("Age:", )
    gui.addField("Gender(m/f/o):", )
    gui.show()
    print(gui.data)
    return gui


def parse_gui(gui):
    participant_number = str(gui.data[0])  # removed int to allow for strings to be insert
    cond_num = int(gui.data[1])
    age = int(gui.data[2])
    gender = (gui.data[3])
    global CONDITION_NUMBER
    CONDITION_NUMBER = cond_num
    global PARTICIPANT_NUMBER
    PARTICIPANT_NUMBER = participant_number
    return participant_number, cond_num, age, gender


def show_dialog_and_get_info():
    print("show_dialog...")
    gui = init_and_show_gui()
    # this is a blocking function. as long as the participant has not clicked ok the code progression
    # will be blocked here
    if gui.OK:
        print("user clicked ok!")
    else:
        print("user clicked cancel!")
        exit()

    available_genders = ['m', 'f',
                         'o']  # I leave here all the genders in case we want to do something with the fathers.
    available_conditions = [1,2]  #both conditions are available
    available_ages = list(range(18,
                                51))  # from 18 to 51 
    print(available_ages)
    try:
        participant_number, cond_num, age, gender = parse_gui(gui)
        if gender not in available_genders:
            error = ValueError('Error: gender not available!', gender, available_genders)
            write_to_log_error_file(error)
            raise error
        if cond_num not in available_conditions:
            error = ValueError('Error: condition not available!', cond_num, available_conditions)
            write_to_log_error_file(error)
            raise error
        if age not in available_ages:
            error = ValueError('Error: age not available!', age, available_ages)
            write_to_log_error_file(error)
            raise error
        return participant_number, cond_num, age, gender
    except ValueError as e:
        print(e)
        write_to_log_error_file(str(e))
        gui_error = psychopy.gui.Dlg(title=u'Error')
        gui_error.addText('Please check the inputed data.')
        gui_error.show()
        if gui_error.OK:
            print("user clicked ok!")
            write_to_log_error_file("user clicked ok!")
            show_dialog_and_get_info()  # now it save just the correct data!!
        else:
            write_to_log_error_file("user clicked cancel!")
            print("user clicked cancel!")
            exit()


def show_message(window, msg):
    try:
        text_stim = psychopy.visual.TextStim(
            win=window,
            text=msg,
            color=(-1, -1, -1), height=30.0)
        text_stim.draw(window)
        window.flip()
    except Exception as e:
        print('error while show_message')
        write_to_log_error_file('error in show_message')
        write_to_log_error_file(str(e))


def show_messages_and_wait(window,
                           cpt):  # extracted from the brackets the components of the time horizon line - put them back if you want it:  , rectangle_time, rectangle_time_passing
    messages = {'welcome': WELCOME,
                # 'break': BREAK,
                'thanks': THANKS,
                'congratulations': CONGRATULATIONS}
    this_message = {0 + OFFSET: 'welcome',
                    # cpt_iteration + OFFSET: 'break',
                    TOTAL_NUMBER_OF_TRIALS + OFFSET: 'thanks',
                    TOTAL_NUMBER_OF_TRIALS + OFFSET + 5: 'congratulations'}  # make it has received the feedback and he starts from new cpt

    try:
        text = messages[this_message[cpt]]
    except KeyError:
        return

    text_stim = psychopy.visual.TextStim(
        win=window,
        text=text,
        color=(-1, -1, -1), height=30.0)
    text_stim.draw(window)
    window.flip()
    psychopy.event.waitKeys(keyList=['space'])
    print("user pressed space -> go to next step !")
    if cpt - 1 == TOTAL_NUMBER_OF_TRIALS or cpt == 1:
        rating_scale(window, cpt)
        rating_scale_temperament(window, cpt)


def show_instructions_and_wait(window, is_reward, cpt):
    try:
        print("is_reward=%s" % is_reward)
        if cpt < 2:
            if is_reward is True:
                print("true")
                instructions_text = INSTRUCTIONS_REWARD_EXP
            elif is_reward is False:
                print("false")
                instructions_text = INSTRUCTIONS_PUNISHMENT_EXP
            print(instructions_text)
            text_stim = psychopy.visual.TextStim(
                win=window,
                text=instructions_text,
                color=(-1, -1, -1), height=30.0)
            text_stim.draw(window)
            window.flip()
            psychopy.event.waitKeys(keyList=['space'])
            print("user pressed space -> go to next step !")
            return is_reward
        else:
            window.flip()
    except Exception as e:
        print('error while show_instructions_and_wait')
        write_to_log_error_file('error in show_instructions_and_wait')
        write_to_log_error_file(str(e))


def get_number_from_string(input_sting):
    #find digit in string
    try:
        digit_found = ''.join([n for n in input_sting if n.isdigit()])
        #transform digit found to actual numerical value that will be use for is_even
        value = int(digit_found)
        return value
    except (ValueError, TypeError) as e:
        #if there is no digit in the string return a random integer
        write_to_log_error_file('could not find digit in string')
        write_to_log_error_file(str(e))

        gui_error = psychopy.gui.Dlg(title=u'Error')
        gui_error.addText('Please check the inputed data.')
        gui_error.show()
        if gui_error.OK:
            print("user clicked ok!")
            write_to_log_error_file("user clicked ok!")
            show_dialog_and_get_info()  # now it save just the correct data!!
        else:
            write_to_log_error_file("user clicked cancel!")
            print("user clicked cancel!")
            exit()


def is_even(participant_number):
    try:
        print('setting if part_num is odd or even')
        if (participant_number % 2) == 0:
            is_even = True
            print("{0} is Even".format(participant_number))
        else:
            is_even = False
            print("{0} is Odd".format(participant_number))
        print("is_even=%s" % is_even)
        return is_even
    except Exception as e:
        write_to_log_error_file('error while is_even')
        write_to_log_error_file(str(e))


def position_arms(window, is_even, toy_bear, toy_duck, pos_left,
                  pos_right):  # switch the position of the toys every 10 trials?
    try:
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
    except Exception as e:
        print('error while position_arms')
        write_to_log_error_file('error in position_arms')
        write_to_log_error_file(str(e))


def init_rating_scale():
    rating_scale = visual.RatingScale(window, low=0,
                                      high=1,
                                      scale='rate the emotion',
                                      size=1.0,
                                      precision=100,
                                      markerStart=0.5,
                                      stretch=2.0,
                                      textColor='Gray',
                                      mouseOnly=True,
                                      showValue=False
                                      )
    rating_scale.acceptBox.pos = [-10, -100]
    return rating_scale


def init_rating_scale_temperament():
    rating_scale = visual.RatingScale(window, low=0,
                                      high=1,
                                      scale='rate the temperament',
                                      size=1.0,
                                      precision=100,
                                      markerStart=0.5,
                                      stretch=2.0,
                                      textColor='Gray',
                                      mouseOnly=True,
                                      showValue=False
                                      )
    rating_scale.acceptBox.pos = [-10, -100]
    return rating_scale


def parse_image_name_from_file(filename):
    if filename == 'baby_happy.png':
        return 1
    if filename == 'baby_neutral.png':
        return 0
    if filename == 'baby_sad.png':
        return -1
    print("error the image file names was updated!!")


def rating_scale(window, cpt):
    QUESTION = "INTRUCTIONS RATING SCALE\n\nRate the emotions!\n\nYou will see 3 different infant faces.\nTry to evaluate as fast as possible the emotion expressed by the following images.\nWhere the left of the scale is very sad and right very happy, and with middle value representing completely neutral.\n\nUse the MOUSE to provide your feedback by clicking one point on the line below the face.\nClick 'accept' to proceed.\nNow press 'space' when you are ready to rate!"
    REMINDER = "Rate an emotion."
    show_message(window, QUESTION)
    psychopy.event.waitKeys(keyList=['space'])

    rating_scale = init_rating_scale()

    offset_y = 130
    happy_face.pos = [happy_face.pos[0], happy_face.pos[1] - offset_y]
    neutral_face.pos = [neutral_face.pos[0], neutral_face.pos[1] - offset_y]
    sad_face.pos = [sad_face.pos[0], sad_face.pos[1] - offset_y]

    text_question = psychopy.visual.TextStim(
        win=window,
        text=REMINDER,
        color=(-1, -1, -1),
        wrapWidth=screen_size[0] / 1.5,
        height=30.0)
    text_question.pos = [text_question.pos[0], sad_face.pos[1] + offset_y * 2]
    text_very_sad = psychopy.visual.TextStim(
        win=window,
        text='Very Sad',
        color=(-1, -1, -1),
        height=30.0)
    text_very_sad.pos = [rating_scale.pos[0] - 600, rating_scale.pos[1] - 140]

    text_very_happy = psychopy.visual.TextStim(
        win=window,
        text='Very Happy',
        color=(-1, -1, -1),
        height=30.0)
    text_very_happy.pos = [rating_scale.pos[0] + 600, rating_scale.pos[1] - 140]

    image_list = [happy_face, neutral_face, sad_face]
    random.shuffle(image_list)

    for image in image_list:
        base_line = parse_image_name_from_file(image._imName)
        rating_scale = init_rating_scale()
        rating = None
        decision_time = None
        while rating_scale.noResponse:
            rating_scale.draw()
            text_question.draw(window)
            text_very_sad.draw(window)
            text_very_happy.draw(window)
            image.draw(window)
            rating = rating_scale.getRating() * 100  # according to cpt you'll know when has been completed
            if rating != 50.0:
                rating_scale.acceptBox.pos = [0, 0]

            decision_time = rating_scale.getRT()
            window.flip()

        print('the rating score is %d, the decision time is %d, the base line face is %d' % (
            rating, decision_time, base_line))
        if cpt == 1:
            initial_ratings.append([rating, decision_time, base_line])
            write_to_log_error_file('initial ratings emotions--> rating=%f decision_time=%f base_line=%i' % (rating, decision_time, base_line))
        else:
            final_ratings.append([rating, decision_time, base_line])
            write_to_log_error_file(
                'final ratings emotions--> rating=%f decision_time=%f base_line=%i' % (rating, decision_time, base_line))

    happy_face.pos = initial_pos
    neutral_face.pos = initial_pos
    sad_face.pos = initial_pos


def rating_scale_temperament(window, cpt):
    QUESTION = "INTRUCTIONS RATING SCALE\n\nRate the temperament!\n\nTry to evaluate the temperament (easy vs difficult baby) of the following infants. Use the mouse to rate the temperament, where at the left of the rating scale is a 'difficult' baby and at the right an 'easy' baby.\n\nUse the MOUSE to provide your feedback by clicking one point on the line below the face.\nClick 'accept' to proceed.\nNow press 'space' when you are ready to rate!"
    REMINDER = "Rate the temperament."
    show_message(window, QUESTION)
    psychopy.event.waitKeys(keyList=['space'])

    try:
        rating_scale_temperament = init_rating_scale_temperament()
    except Exception as e:
        write_to_log_error_file('error while init_rating_scale_temperament')
        write_to_log_error_file(str(e))

    offset_y = 130
    happy_face.pos = [happy_face.pos[0], happy_face.pos[1] - offset_y]
    neutral_face.pos = [neutral_face.pos[0], neutral_face.pos[1] - offset_y]
    sad_face.pos = [sad_face.pos[0], sad_face.pos[1] - offset_y]

    text_question = psychopy.visual.TextStim(
        win=window,
        text=REMINDER,
        color=(-1, -1, -1),
        wrapWidth=screen_size[0] / 1.5,
        height=30.0)
    text_question.pos = [text_question.pos[0], sad_face.pos[1] + offset_y * 2]
    text_very_difficult = psychopy.visual.TextStim(
        win=window,
        text='Very Difficult',
        color=(-1, -1, -1),
        height=30.0)
    text_very_difficult.pos = [rating_scale_temperament.pos[0] - 600, rating_scale_temperament.pos[1] - 140]

    text_very_easy = psychopy.visual.TextStim(
        win=window,
        text='Very Easy',
        color=(-1, -1, -1),
        height=30.0)
    text_very_easy.pos = [rating_scale_temperament.pos[0] + 600, rating_scale_temperament.pos[1] - 140]

    image_list = [happy_face, neutral_face, sad_face]
    random.shuffle(image_list)

    for image in image_list:
        base_line_temperament = parse_image_name_from_file(image._imName)
        rating_scale_temperament = init_rating_scale()
        rating_temperament = None
        decision_time_temperament = None
        while rating_scale_temperament.noResponse:
            rating_scale_temperament.draw()
            text_question.draw(window)
            text_very_difficult.draw(window)
            text_very_easy.draw(window)
            image.draw(window)
            rating_temperament = rating_scale_temperament.getRating() * 100  # according to cpt you'll know when has been completed
            if rating_temperament != 50.0:
                rating_scale_temperament.acceptBox.pos = [0, 0]

            decision_time_temperament = rating_scale_temperament.getRT()
            window.flip()

        print('the rating score is %d, the decision time is %d, the base line face is %d' % (
            rating_temperament, decision_time_temperament, base_line_temperament))
        if cpt == 1:
            initial_ratings_temperament.append([rating_temperament, decision_time_temperament, base_line_temperament])
            write_to_log_error_file('initial ratings temperament--> rating=%f decision_time=%f base_line=%i'
                                    % (rating_temperament, decision_time_temperament, base_line_temperament))
        else:
            final_ratings_temperament.append([rating_temperament, decision_time_temperament, base_line_temperament])
            write_to_log_error_file('final ratings temperament--> rating=%f decision_time=%f base_line=%i'
                                    % (rating_temperament, decision_time_temperament, base_line_temperament))

    happy_face.pos = initial_pos
    neutral_face.pos = initial_pos
    sad_face.pos = initial_pos


def experiment_trial(is_reward, window, right_highlight, left_highlight, toy_bear, toy_duck,
                     happy_face, neutral_face, sad_face,
                     cpt_iteration):  # remoted time horizon from the brackets, if you want it put it back :  , rectangle_time, rectangle_time_passing
    #try:
        print("start experiment trial with is_reward=%s..." % is_reward)
        fixation_cross.draw(window)
        # rectangle_time.draw(window)   #no show of time passing
        # rectangle_time_passing.draw(window)
        window.flip()
        core.wait(0.3)
        print("waited 300 ms.")
        fixation_cross.draw(window)
        #  rectangle_time.draw(window)                      #no show of time passing
        #  rectangle_time_passing.draw(window)
        window.flip()
        core.wait(0.3)
        print("waited 300 ms.")
        # remove fixation cross
        #  rectangle_time.draw(window)                      #no show of time passing
        #  rectangle_time_passing.draw(window)
        window.flip()
        if is_reward is True:
            sad_face.draw(window)

        elif is_reward is False:
            happy_face.draw(window)

        toy_bear.draw(window)  # do not show toys while feeback is on
        toy_duck.draw(window)  # do not show toys while feeback is on
        #   rectangle_time.draw(window)                                             #no show of time passing
        #   rectangle_time_passing.draw(window)
        window.flip()
        start = time.time()
        response = psychopy.event.waitKeys(
            keyList=['left', 'right', 'escape'])  # add break if they press space\ removed space
        end = time.time()
        reaction_time = end - start
        print('reaction time is', reaction_time)
        reaction_times_experiment.append(reaction_time)

        if len(response) > 1:
            response = response[:-1]

        print(response)
        # highlight selected items
        pressed_left = None  # creates problem because sometimes it doesn't register pressed left

        if 'left' in response:
            pressed_left = True
            left_highlight.draw(window)
        if 'right' in response:
            pressed_left = False
            right_highlight.draw(window)
        #  if 'space' in response:  #added break
        #     continueRoutine = False
        #     show_message(window, BREAK)
        #     psychopy.event.waitKeys(keyList=['space'])  #CHECK WHY IS SKIPPING ONE TRIAL
        #     continueRoutine = True


        toy_bear.draw(window)
        toy_duck.draw(window)
        #   rectangle_time.draw(window)                   #no show of time passing
        #  rectangle_time_passing.draw(window)
        window.flip()
        feedback_value = feedback(window, toy_bear, toy_duck, happy_face, neutral_face, sad_face, pressed_left, cpt_iteration)
        # pressed_pauses.append(pressed_pause)
        pressed_lefts.append(pressed_left)

        #save to log file
        write_to_log_error_file("reaction_time=%s press_left=%s feedback=%s"
                                % (reaction_time, str(pressed_left), feedback_value))
        if 'escape' in response:
            print('exit...')
            save_progress()
            exit()
            #save_progress()
            #window.close()
            #core.quit()
            #exit()
    #except Exception as e:
    #    print('error while experiment_trial')
    #    write_to_log_error_file('error in experiment_trial')
    #    write_to_log_error_file(str(e))


# decide which baby face to display
def feedback(window, toy_bear, toy_duck, happy_face, neutral_face,
             sad_face, pressed_left, cpt_iteration):
    print('start feedback...')
    # for right_outcome in range(0, len(right_outcomes)):
    #   print (right_outcomes[right_outcome])
    # for left_outcome in range(0, len(left_outcomes)):
    #     print (left_outcomes[left_outcome])
    right_outcome = right_outcomes[cpt_iteration - 1]  # not random anymore: removed random.choice(right_outcomes)
    left_outcome = left_outcomes[cpt_iteration - 1]
    print("right_outcome=%d and left_outcome=%d" % (right_outcome, left_outcome))

    if pressed_left:
        print('is_reward=%s' % is_reward)
        print('pressed_left')
        feedback_value = left_outcome  # not random anymore: removed rnd_left_outcome
    else:
        print('is_reward=%s' % is_reward)
        print('pressed_right')
        feedback_value = right_outcome
    print('feedback is % d' % feedback_value)

    core.wait(0.6)
    print("waited 600 ms.")

    if feedback_value == -1:
        sad_face.draw(win=window)
    if feedback_value == 1:
        happy_face.draw(win=window)
    if feedback_value == 0:
        neutral_face.draw(win=window)

    #  toy_bear.draw(window)  #do not show toys while feedbacks are on
    #  toy_duck.draw(window)  #do not show toys while feedbacks are on

    feedbacks.append(str(feedback_value))

    #  rectangle_time.draw(window)                    #no show of time passing
    #  rectangle_time_passing.draw(window)
    window.flip()
    core.wait(1)
    return str(feedback_value)


# def compute_progress(rectangle_time, rectangle_time_passing, cpt):   #use bloks with % of task completed?   # COMMENTED THE FUNCTION THAT MEDA APPEAR THE TIME HORIZON LINE, IF YOU WANT IT BACK UNCOMMENT
#    progress = (cpt/TOTAL_NUMBER_OF_TRIALS)*rectangle_time.width
#    print("progress is %d" % progress)
#    if progress > rectangle_time.width:
#       progress = rectangle_time.width

#   rectangle_time_passing.width = progress/1.5
#   rectangle_time_passing.pos[0] = -500 + rectangle_time_passing.width/2


def create_directory(name):
    current_directory = os.getcwd()
    final_directory = os.path.join(current_directory, r'%s' % name)
    if not os.path.exists(final_directory):
        os.makedirs(final_directory)


def write_to_log_error_file(error):
    log_error_file = open("log_error.txt", "a")
    timestamp = str(datetime.datetime.now())
    log_error_file.write("%s:%d:%s: %s\n" % (PARTICIPANT_NUMBER, CONDITION_NUMBER, timestamp, error))
    log_error_file.close()

def remove_none(d):
    return ['None' if v is None else v for v in d] 
    
def init_to_999(a):
    return [999 if x==1 else 999 for x in a]

def save_progress():
    # Store info about the experiment session
    expName = 'bandit_exp'
    expInfo = {'gui': {'participant_number': participant_number, 'cond_num': cond_num, 'age': age, 'gender': gender},
               'date': data.getDateStr(), 'expName': expName}

    directory_name = 'Data cognitive task'
    create_directory(directory_name)

    filename = directory_name + '/' + '%s_%s_%s.xlsx' % (participant_number, expName, expInfo['date'])
    print('filepath is %s' % filename)

    list_name = ['bandit_task', 'rating']

    try:
        workbook = xlsxwriter.Workbook(filename)
    except Exception as e:
        print('error while creating workbook')
        write_to_log_error_file('error while creating workbook')
        write_to_log_error_file(str(e))
        exit()

    try:
        print('final_ratings.....')
        global final_ratings
        global final_ratings_temperament
        global feedbacks
        global initial_ratings
        global initial_ratings_temperament
        global pressed_lefts
        global reaction_times_experiment

        if not final_ratings:
            final_ratings = [ init_to_999(initial_ratings[0]), init_to_999(initial_ratings[1]), init_to_999(initial_ratings[2]) ]
                
        if not final_ratings_temperament:
            final_ratings_temperament = final_ratings
                
        print(reaction_times_experiment)
        print(feedbacks)
        print(pressed_lefts)
        print(initial_ratings)
        print(final_ratings)
        print(initial_ratings_temperament)
        print(final_ratings_temperament)
        print('********************')
        
        
        feedbacks = remove_none(feedbacks)
        pressed_lefts = remove_none(pressed_lefts)
        initial_ratings = remove_none(initial_ratings)
        final_ratings = remove_none(final_ratings)
        initial_ratings_temperament = remove_none(initial_ratings_temperament)
        final_ratings_temperament = remove_none(final_ratings_temperament)
        
        print(reaction_times_experiment)
        print(feedbacks)
        print(pressed_lefts)
        print(initial_ratings)
        print(final_ratings)
        print(initial_ratings_temperament)
        print(final_ratings_temperament)
        
        row = 0
        col = 0
        for sheet_name in list_name:
            worksheet = workbook.add_worksheet(sheet_name)
            if sheet_name == 'bandit_task':
                row_headers = ['participant_num', 'cond_num', 'cpt_iteration', 'reaction_times', 'feedbacks',
                               'pressed_left', 'age', 'gender']
                worksheet.write_row(row, col, tuple(row_headers))
                for i in range(0, len(reaction_times_experiment)):
                    row += 1
                    worksheet.write_row(row, col,
                                        tuple((participant_number, cond_num, i, reaction_times_experiment[i], feedbacks[i],
                                               pressed_lefts[i], age, gender)))

            if sheet_name == 'rating':
                row = 0
                row_headers = ['initial_base_line', 'initial_rating_score', 'initial_reaction_time',
                               'final_base_line', 'final_rating_score', 'final_reaction_time',
                               'initial_base_line_temperament', 'initial_rating_score_temperament',
                               'initial_reaction_time_temperament',
                               'final_base_line_temperament', 'final_rating_score_temperament',
                               'final_reaction_time_temperament']
                worksheet.write_row(row, col, tuple(row_headers))
                for i in range(0, len(initial_ratings)):
                    row += 1
                    
                    print('i', i)
                    print(row, col)
                    print(initial_ratings[i][2], initial_ratings[i][0], initial_ratings[i][1])
                    print('****')
                    print(final_ratings)
                    print(final_ratings[i])
                    print(final_ratings[i][2], final_ratings[i][0], final_ratings[i][1])
                    print('****')
                    print(initial_ratings_temperament[i][2], initial_ratings_temperament[i][0],initial_ratings_temperament[i][1])
                    print('****')
                    print(final_ratings_temperament[i][2], final_ratings_temperament[i][0], final_ratings_temperament[i][1])
                    print('****')
                    print('****')
                    
                    t = tuple((initial_ratings[i][2], initial_ratings[i][0], initial_ratings[i][1],
                                               final_ratings[i][2], final_ratings[i][0], final_ratings[i][1],
                                               initial_ratings_temperament[i][2], initial_ratings_temperament[i][0],
                                               initial_ratings_temperament[i][1],
                                               final_ratings_temperament[i][2], final_ratings_temperament[i][0],
                                               final_ratings_temperament[i][1]))
                    print(t)
                    worksheet.write_row(row, col, t)
    except Exception as e:
        print('error while writing in workbook')
        write_to_log_error_file('error while writing in workbook')
        write_to_log_error_file(str(e))
        exit()
    exit()
    workbook.close()
    core.quit()
    core.close()


if __name__ == "__main__":

    #event.globalKeys.add(key='escape', func=save_progress, name='shutdown')

    try:
        right_outcomes, left_outcomes = load_conditions()
    except Exception as e:
        print('error while loading conditions')
        write_to_log_error_file('error while loading conditions')
        write_to_log_error_file(str(e))

    print("start experiment...")
    participant_number, cond_num, age, gender = show_dialog_and_get_info()
    print("participant name is %s, cond_num is %d, age is %d, gender is %s."
          % (participant_number, cond_num, age, gender))
    if cond_num == 1:
        is_reward = True
    elif cond_num == 2:
        is_reward = False

    is_even_value = is_even(get_number_from_string(participant_number))
    print('is_even_value', is_even_value)

    window, rectangle_right, rectangle_left, toy_bear, toy_duck, happy_face, neutral_face, sad_face, fixation_cross, right_highlight, left_highlight = init_elements_in_window()  # REMOVED , rectangle_time, rectangle_time_passing   PUT BACK if you want time horizon

    position_arms(window, is_even_value, toy_bear, toy_duck, pos_left, pos_right)

    print("windows elements are ready for use.")

    cpt_iteration = 1
    while True:
        print("before show message")
        show_messages_and_wait(window, cpt_iteration)  # removed:   , rectangle_time, rectangle_time_passing   put it back if you want the time horizon
        show_instructions_and_wait(window, is_reward, cpt_iteration)

        if cpt_iteration == TOTAL_NUMBER_OF_TRIALS + OFFSET:  # to have N you need to put n+1
            break
        experiment_trial(is_reward, window, right_highlight, left_highlight, toy_bear, toy_duck,
                         happy_face, neutral_face, sad_face,
                         cpt_iteration)  # removed:   , rectangle_time, rectangle_time_passing   ## put it back in the line below if you want the time horizon:  # compute_progress(rectangle_time, rectangle_time_passing, cpt_iteration)  #don't need this line because we "silenced" the function for compute progress
        cpt_iteration += 1
        print("%d experiment trials has been performed." % (cpt_iteration - 1))

    show_message(window, CONGRATULATIONS)
    core.wait(2)
    save_progress()