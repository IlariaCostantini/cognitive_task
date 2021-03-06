   #07/05/2019 definitive version
# Author: Ilaria Costantini

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

logging.console.setLevel(logging.DEBUG)

TOTAL_NUMBER_OF_TRIALS = 200
OFFSET = 1

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




def load_conditions():
    """
    load conditions
    """
    print("system platform is = %s" % sys.platform)
    file_path = {
        'condition': r'condition.xlsx'
    }

    if sys.platform.startswith('macOS'):  # are these the right info?
        file_path = {'condition': r'..O:\bandit_task\bandit_task\condition.xlsx'}

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


WELCOME = "Welcome to our study.\n\nThanks for taking part to this experiment!" \
          "\nFirstly you will be asked to rate the emotion and the temperament of some infant faces and then to proceed to the main experiment." \
          "\n\nPlease press the'SPACE' bar to continue"
BREAK = "You are doing great,\n\nYou are in a paused mood.\nPress the 'SPACE' bar when you are ready to continue..."
THANKS = "Congratulations!!!\n\nyou have completed this session. Please take few seconds to rate the following images.\n\nYou contribution is really valuable to us!\n\n Press 'SPACE' to proceed."
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


def init_elements_in_window():
    window = init_window()

    rectangle_right = psychopy.visual.Rect(win=window, units="pix", width=toy_size[0] + 10, height=toy_size[1] + 10,
                                           lineColor='green', colorSpace='rgb', pos=pos_right)
    rectangle_left = psychopy.visual.Rect(win=window, units="pix", width=toy_size[0] + 10, height=toy_size[1] + 10,
                                          lineColor='green', colorSpace='rgb', pos=pos_left)
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
    right_highlight = psychopy.visual.Rect(win=window, pos=pos_right, width=250, height=250, color=(0.0, 1.0, 0.0),
                                           units='pix')
    left_highlight = psychopy.visual.Rect(win=window, pos=pos_left, width=250, height=250, color=(0.0, 1.0, 0.0),
                                          units='pix')

    rectangle_time = visual.Rect(win=window, name='rectangle_time', width=1000, height=50, ori=0,
                                 pos=(0, -500),
                                 lineWidth=3, lineColor=[-1, -1, -1], lineColorSpace='rgb', fillColor=[0, 0, 0],
                                 fillColorSpace='rgb',
                                 opacity=1, depth=0.0, interpolate=True)

    rectangle_time_passing = visual.Rect(win=window, name='rectangle_time_passing', width=0,
                                         height=50, ori=0, pos=(-500, -500), lineWidth=3,
                                         lineColor=[-1, -1, -1], lineColorSpace='rgb', fillColor=(0.0, 1.0, 0.0),
                                         fillColorSpace='rgb',
                                         opacity=1, depth=-1.0, interpolate=True)

    return window, rectangle_right, rectangle_left, toy_bear, toy_duck, happy_face, neutral_face, sad_face, fixation_cross, right_highlight, left_highlight, rectangle_time, rectangle_time_passing


def init_window():
    window = psychopy.visual.Window(
        units='pix',
        size=screen_size,
        fullscr=True,
        # change in True when you run the actual experiment and change the screen size into the actual size of the screen of the pc you will use
        color=[0, 0, 0])
    return window


def init_and_show_gui():
    gui = psychopy.gui.Dlg()
    gui.addField("Participant Number:", "")
    gui.addField("Condition Number:", )
    gui.addField("Age:", )
    gui.addField("Gender(m/f/o):", "")
    gui.show()
    print(gui.data)
    return gui


def parse_gui(gui):
    participant_number = int(gui.data[0])
    cond_num = int(gui.data[1])
    age = int(gui.data[2])
    gender = (gui.data[3])
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

    available_genders = ['m', 'f', 'o']
    available_conditions = [1, 2]
    available_ages = list(range(18, 51))
    print(available_ages)
    try:
        participant_number, cond_num, age, gender = parse_gui(gui)
        if gender not in available_genders:
            raise ValueError('Error: gender not available!', gender, available_genders)
        if cond_num not in available_conditions:
            raise ValueError('Error: condition not available!', cond_num, available_conditions)
        if age not in available_ages:
            raise ValueError('Error: age not available!', age, available_ages)

    except ValueError as e:
        print(e)
        gui_error = psychopy.gui.Dlg(title=u'Error')
        gui_error.addText('Please check the inputed data.')
        gui_error.show()
        if gui_error.OK:
            print("user clicked ok!")
            show_dialog_and_get_info()  # now it save just the correct data!!
        else:
            print("user clicked cancel!")
            exit()

    return participant_number, cond_num, age, gender


def show_message(window, msg):
    text_stim = psychopy.visual.TextStim(
        win=window,
        text=msg,
        color=(-1, -1, -1), height=30.0)
    text_stim.draw(window)
    window.flip()


def show_messages_and_wait(window, cpt, rectangle_time, rectangle_time_passing):
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


def is_even(participant_number):
    print('setting if part_num is odd or even')
    if (participant_number % 2) == 0:
        is_even = True
        print("{0} is Even".format(participant_number))
    else:
        is_even = False
        print("{0} is Odd".format(participant_number))
    print("is_even=%s" % is_even)
    return is_even


def position_arms(window, is_even, toy_bear, toy_duck, pos_left, pos_right):
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
        else:
            final_ratings.append([rating, decision_time, base_line])

    happy_face.pos = initial_pos
    neutral_face.pos = initial_pos
    sad_face.pos = initial_pos


def rating_scale_temperament(window, cpt):
    QUESTION = "INTRUCTIONS RATING SCALE\n\nRate the temperament!\n\nTry to evaluate the temperament (easy vs difficult baby) of the following infants. Use the mouse to rate the temperament, where at the left of the rating scale is an 'easy' baby and at the right a 'difficult' baby.\n\nUse the MOUSE to provide your feedbcak by clicking one point on the line below the face.\nClick 'accept' to proceed.\nNow press 'space' when you are ready to rate!"
    REMINDER = "Rate the temperament."
    show_message(window, QUESTION)
    psychopy.event.waitKeys(keyList=['space'])

    rating_scale_temperament = init_rating_scale_temperament()

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
        else:
            final_ratings_temperament.append([rating_temperament, decision_time_temperament, base_line_temperament])

    happy_face.pos = initial_pos
    neutral_face.pos = initial_pos
    sad_face.pos = initial_pos


def experiment_trial(is_reward, window, right_highlight, left_highlight, toy_bear, toy_duck,
                     happy_face, neutral_face, sad_face, cpt_iteration, rectangle_time, rectangle_time_passing):
    print("start experiment trial with is_reward=%s..." % is_reward)
    fixation_cross.draw(window)
    rectangle_time.draw(window)
    rectangle_time_passing.draw(window)
    window.flip()
    core.wait(0.5)
    print("waited 500 ms.")
    fixation_cross.draw(window)
    rectangle_time.draw(window)
    rectangle_time_passing.draw(window)
    window.flip()
    core.wait(0.5)
    print("waited 500 ms.")
    # remove fixation cross
    rectangle_time.draw(window)
    rectangle_time_passing.draw(window)
    window.flip()
    if is_reward is True:
        sad_face.draw(window)

    elif is_reward is False:
        happy_face.draw(window)

    toy_bear.draw(window)
    toy_duck.draw(window)
    rectangle_time.draw(window)
    rectangle_time_passing.draw(window)
    window.flip()
    start = time.time()
    response = psychopy.event.waitKeys(
        keyList=['left', 'right', 'escape'])  # add break if they press space\ removed space
    end = time.time()
    reaction_time = end - start
    print('reaction time is', reaction_time)
    reaction_times_experiment.append(reaction_time)

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
    if 'escape' in response:
        window.close()
        core.quit()

    toy_bear.draw(window)
    toy_duck.draw(window)
    rectangle_time.draw(window)
    rectangle_time_passing.draw(window)
    window.flip()
    feedback(window, toy_bear, toy_duck, happy_face, neutral_face, sad_face, pressed_left, cpt_iteration)
    # pressed_pauses.append(pressed_pause)
    pressed_lefts.append(pressed_left)


# decide which baby face to display
def feedback(window, toy_bear, toy_duck, happy_face, neutral_face,
             sad_face, pressed_left, cpt_iteration):
    print('start feedback...')
    # for right_outcome in range(0, len(right_outcomes)):
    #   print (right_outcomes[right_outcome])
    # for left_outcome in range(0, len(left_outcomes)):
    #     print (left_outcomes[left_outcome])
    right_outcome = right_outcomes[cpt_iteration-1]  # not random anymore: removed random.choice(right_outcomes)
    left_outcome = left_outcomes[cpt_iteration-1]
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

    core.wait(0.5)

    if feedback_value == -1:
        sad_face.draw(win=window)
    if feedback_value == 1:
        happy_face.draw(win=window)
    if feedback_value == 0:
        neutral_face.draw(win=window)

    toy_bear.draw(window)
    toy_duck.draw(window)

    feedbacks.append(str(feedback_value))
    rectangle_time.draw(window)
    rectangle_time_passing.draw(window)
    window.flip()
    core.wait(1)


def compute_progress(rectangle_time, rectangle_time_passing, cpt):
    progress = (cpt/TOTAL_NUMBER_OF_TRIALS)*rectangle_time.width
    print("progress is %d" % progress)
    if progress > rectangle_time.width:
        progress = rectangle_time.width

    rectangle_time_passing.width = progress/1.5
    rectangle_time_passing.pos[0] = -500 + rectangle_time_passing.width/2


def create_directory(name):
    current_directory = os.getcwd()
    final_directory = os.path.join(current_directory, r'%s' % name)
    if not os.path.exists(final_directory):
        os.makedirs(final_directory)


if __name__ == "__main__":

    event.globalKeys.add(key='escape', func=core.quit, name='shutdown')
    right_outcomes, left_outcomes = load_conditions()

    print("start experiment...")
    participant_number, cond_num, age, gender = show_dialog_and_get_info()
    print("participant name is %s, cond_num is %d, age is %d, gender is %s."
          % (participant_number, cond_num, age, gender))
    if cond_num == 1:
        is_reward = True
    elif cond_num == 2:
        is_reward = False
    window, rectangle_right, rectangle_left, toy_bear, toy_duck, happy_face, neutral_face, sad_face, fixation_cross, right_highlight, left_highlight, rectangle_time, rectangle_time_passing = init_elements_in_window()

    position_arms(window, is_even(participant_number), toy_bear, toy_duck, pos_left, pos_right)

    print("windows elements are ready for use.")

    cpt_iteration = 1
    while True:
        print("before show message")
        show_messages_and_wait(window, cpt_iteration, rectangle_time, rectangle_time_passing)
        show_instructions_and_wait(window, is_reward, cpt_iteration)

        if cpt_iteration == TOTAL_NUMBER_OF_TRIALS + OFFSET:  # to have N you need to put n+1
            break
        experiment_trial(is_reward, window, right_highlight, left_highlight, toy_bear, toy_duck,
                         happy_face, neutral_face, sad_face, cpt_iteration, rectangle_time, rectangle_time_passing)
        compute_progress(rectangle_time, rectangle_time_passing, cpt_iteration)
        cpt_iteration += 1
        print("%d experiment trials has been performed." % (cpt_iteration - 1))

    show_message(window, CONGRATULATIONS)
    core.wait(2)

    # Store info about the experiment session
    expName = 'bandit_exp'
    expInfo = {'gui': {'participant_number': participant_number, 'cond_num': cond_num, 'age': age, 'gender': gender},
               'date': data.getDateStr(), 'expName': expName}

    directory_name = 'Data cognitive task'
    create_directory(directory_name)

    filename = directory_name + '/' + '%d_%s_%s.xlsx' % (participant_number, expName, expInfo['date'])
    print('filepath is %s' % filename)

    list_name = ['bandit_task', 'rating']

    workbook = xlsxwriter.Workbook(filename)
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
                worksheet.write_row(row, col,
                                    tuple((initial_ratings[i][2], initial_ratings[i][0], initial_ratings[i][1],
                                           final_ratings[i][2], final_ratings[i][0], final_ratings[i][1],
                                           initial_ratings_temperament[i][2], initial_ratings_temperament[i][0],
                                           initial_ratings_temperament[i][1],
                                           final_ratings_temperament[i][2], final_ratings_temperament[i][0], final_ratings_temperament[i][1])))
 
    workbook.close()
    core.quit()
    core.close()