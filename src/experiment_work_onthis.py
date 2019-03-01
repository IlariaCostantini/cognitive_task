import psychopy
import psychopy.gui
import xlrd
import random
from random import randint
from psychopy import core, visual, data, event, logging, clock
# instructions experimental block of reward condition (soothe the baby)
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

NUM_TRIALS = 200

def init_elements_in_window():
    window = init_window()
    pos_right = [200, -200]
    pos_left = [-200, -200]
    toy_size = [200, 200]
    face_size = [150, 200]
    fixationcross_size = [50, 50]
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


def get_random_instructions(instruction_list):
    result = random.choice(instruction_list)
    text = result[0]
    id = result[1]
    print("instruction text is %s. id is %s" % (text, id))
    return text, id


def show_instructions_and_wait(window):
    instruction_list = [(INSTRUCTIONS_REWARD_EXP, True), (INSTRUCTIONS_PUNISHMENT_EXP, False)]
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


def experiment_trial(is_reward, window, right_highlight, left_highlight, toy1, toy2, happy_face, neutral_face, sad_face):
    print("start experiment trial with is_reward=%s..." % is_reward)
    fixation_cross.draw(window)
    window.flip()
    core.wait(1)
    print("waited 1 seconds.")
    fixation_cross.draw(window)
    window.flip()
    core.wait(1)
    # remove fixation cross
    window.flip()
    # right_highlight.draw(window)
    toy1.draw(window)
    toy2.draw(window)
    window.flip()

    response = psychopy.event.waitKeys(keyList=['left', 'right'])
    print(response)
    # highlight selected items
    pressed_left = None
    if 'left' in response:
        pressed_left = True
        left_highlight.draw(window)
        toy2.draw(window)
        toy1.draw(window)
    if 'right' in response:
        pressed_left = False
        right_highlight.draw(window)
        toy1.draw(window)
        toy2.draw(window)
    window.flip()

    # decide what baby face to display to user
    process_result_and_wait(window, happy_face, neutral_face, sad_face, pressed_left, left_highlight, right_highlight, toy1, toy2)


def process_result_and_wait(window, happy_face, neutral_face, sad_face, pressed_left, left_highlight, right_highlight, toy1, toy2):
    #redraw previous state
    if pressed_left:
        left_highlight.draw(window)
        toy2.draw(window)
        toy1.draw(window)
    else:
        right_highlight.draw(window)
        toy1.draw(window)
        toy2.draw(window)

    #decide which baby face to display
    random_id = randint(1, 3)
    if random_id == 1:
        happy_face.draw(window)
    if random_id == 2:
        neutral_face.draw(window)
    if random_id == 3:
        sad_face.draw(window)

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

