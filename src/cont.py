import psychopy
import psychopy.gui
import xlrd
import random
from random import randint
from psychopy import core, visual, data, event, logging, clock

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

NUM_TRIALS = 200

def init_elements_in_window():
    window = init_window()
    pos_right = [200, -200]
    pos_left = [-200, -200]
    grating_size = [200, 200]
    money_size = [150, 200]
    fixationcross_size = [50, 50]
    rectangle_right = psychopy.visual.Rect(win=window, units="pix", width=grating_size[0] + 10, height=grating_size[1] + 10,
                                           lineColor='green', colorSpace='rgb', pos=pos_right)
    rectangle_left = psychopy.visual.Rect(win=window, units="pix", width=grating_size[0] + 10, height=grating_size[1] + 10,
                                          lineColor='green', colorSpace='rgb', pos=pos_left)
    grating_h = psychopy.visual.ImageStim(win=window, image="gratings_h.png", 
                                          color=(1.0, 1.0, 1.0), size=grating_size, units='pix', pos=pos_right)
    grating_v = psychopy.visual.ImageStim(win=window, image="gratings_v.png", 
                                          color=(1.0, 1.0, 1.0), size=grating_size, units='pix', pos=pos_left)
    plus_one = psychopy.visual.ImageStim(win=window, image="plus_one.png", color=(1.0, 1.0, 1.0),
                                          size=money_size,
                                          units='pix', pos=[0, 150])
    zero_pound = psychopy.visual.ImageStim(win=window, image="zero_pound.png", color=(1.0, 1.0, 1.0),
                                            size=money_size,
                                            units='pix', pos=[0, 150])
    minus_one = psychopy.visual.ImageStim(win=window, image="minus_one.png", color=(1.0, 1.0, 1.0), size=money_size,
                                        units='pix', pos=[0, 150])
    fixation_cross = psychopy.visual.ImageStim(win=window, image="fix_cros.png", color=(1.0, 1.0, 1.0),
                                               size=fixationcross_size, units='pix', pos=[0, 150])

    right_highlight = psychopy.visual.Rect(win=window, pos=pos_right, width=250, height=250, color=(0.0, 1.0, 0.0),
                                           units='pix')

    left_highlight = psychopy.visual.Rect(win=window, pos=pos_left, width=250, height=250, color=(0.0, 1.0, 0.0),
                                          units='pix')

    return window, rectangle_right, rectangle_left, grating_h, grating_v, plus_one, zero_pound, minus_one, fixation_cross, right_highlight, left_highlight


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
    gui.addField("Participant Name:", "Ilaria")
    gui.addField("Condition Number:", 1)
    gui.addField("Age:", 26)
    gui.addField("Gender(m/f/o):", "f")
    # this is a blocking function. as long as the participant has not clicked ok the code progression
    # will be blocked here
    gui.show()
    participant_number = gui.data[0]
    cond_num = int(gui.data[1])
    age = int(gui.data[2])
    gender = (gui.data[3])
    return participant_number, cond_num, age, gender

def get_random_messages(messages_list):
    result = random.choice(messages_list)
    text = result[0]
    id = result[1]
    print("instruction text is %s. id is %s" % (text, id))
    return text, id

def show_messages_and_wait(window):
    messages_list = [(WELCOME, True), (BREAK, False), (THANKS, False)]
    messages_text, is_reward = get_random_messages(messages_list)
    text_stim = psychopy.visual.TextStim(
        win=window,
        text=messages_text,
        color=(-1, -1, -1), height=30.0)
    text_stim.draw(window)
    window.flip()
    psychopy.event.waitKeys(keyList=['space'])
    print("user pressed space -> go to next step !")
    return is_reward

def get_random_instructions(instruction_list):
    result = random.choice(instruction_list)
    text = result[0]
    id = result[1]
    print("instruction text is %s. id is %s" % (text, id))
    return text, id

def show_instructions_and_wait(window):
    instruction_list = [(INSTRUCTIONS_REWARD_CONTR, True), (INSTRUCTIONS_PUNISHMENT_CONTR, False)]
    instructions_text, is_reward = get_random_instructions(instruction_list)
    text_stim = psychopy.visual.TextStim(
        win=window,
        text=instructions_text,
        color=(-1, -1, -1), height=30.0)
    text_stim.draw(window)
    window.flip()
    psychopy.event.waitKeys(keyList=['space'])
    print("user pressed space -> go to next step !")
    return is_reward

def experiment_trial(is_reward, window, right_highlight, left_highlight, grating_h, grating_v, plus_one, zero_pound, minus_one):
    print("start experiment trial with is_reward=%s..." % is_reward)
    fixation_cross.draw(window)
    window.flip()
    core.wait(1)
    print("waited 1 seconds.")
    fixation_cross.draw(window)
    window.flip()
    core.wait(0.5)
    print("waited 500 ms.")
    # remove fixation cross
    window.flip()
    # right_highlight.draw(window)
    if is_reward is True:
        minus_one.draw(window)
        grating_v.draw(window)
        grating_h.draw(window)
    elif is_reward is False:
        zero_pound.draw(window)
        grating_v.draw(window)
        grating_h.draw(window)

    window.flip()

    response = psychopy.event.waitKeys(keyList=['left', 'right'])
    print(response)
    # highlight selected items
    pressed_left = None
    if 'left' in response:
        pressed_left = True
        left_highlight.draw(window)
        grating_v.draw(window)
        grating_h.draw(window)
    if 'right' in response:
        pressed_left = False
        right_highlight.draw(window)
        grating_v.draw(window)
        grating_h.draw(window)
    window.flip()

    # decide what baby face to display to user
    process_result_and_wait(window, plus_one, zero_pound, minus_one, pressed_left, left_highlight, right_highlight, grating_v, grating_h)

def process_result_and_wait(window, plus_one, zero_pound, minus_one, pressed_left, left_highlight, right_highlight, grating_v, grating_h):
    #redraw previous state
    if pressed_left:
        left_highlight.draw(window)
        grating_v.draw(window)
        grating_h.draw(window)
    else:
        right_highlight.draw(window)
        grating_v.draw(window)
        grating_h.draw(window)

    #decide which baby face to display
    random_id = randint(1, 3)
    if random_id == 1:
        core.wait(0.5)
        plus_one.draw(window)
    if random_id == 2:
        core.wait(0.5)
        zero_pound.draw(window)
    if random_id == 3:
        core.wait(0.5)
        minus_one.draw(window)

    window.flip()
    core.wait(3)

if __name__ == "__main__":
    print("start experiment...")
    participant_number, cond_num, age, gender = show_dialog_and_get_info()
    print("participant name is %s, cond_num is %d, age is %d, gender is %s."
          % (participant_number, cond_num, age, gender))

    window, rectangle_right, rectangle_left, toy_bear, toy_duck, happy_face, neutral_face, sad_face, fixation_cross, right_highlight, left_highlight = init_elements_in_window()
    print("windows elements are ready for use.")

    is_reward = show_instructions_and_wait(window)

    cpt_iteration = 0
    while True:
        experiment_trial(is_reward, window, right_highlight, left_highlight, toy_bear, toy_duck, happy_face, neutral_face, sad_face)
        cpt_iteration += 1
        print("%d experiment trials has been performed." % cpt_iteration)
