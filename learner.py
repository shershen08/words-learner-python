import exportcsv

import random
import os
import sys
from time import sleep
from gtts import gTTS
import pyglet

pyglet.lib.load_library('avbin')
pyglet.have_avbin=True

# set global flags
lang_from = 'en'
lang_to = 'en'
flag_do_sound = True
flag_do_write = True
number_words = 10

#global var 
results = []

def ask_words_list(total_words_toask=number_words):
    """
    iterates certain amount of word lines between start and (start + limit)
    """

    start = 5
    sheet = exportcsv.read_words_list()
    global results

    for i, row in enumerate(sheet.rows):
        if i > start and i <=int(total_words_toask) + start:
            results.append(do_step(i, (row[0].value, row[1].value)))

def ask_random_words_list(total_words_toask=number_words):
    """
    checks words from random parts of the list
    """
    global results

    sheet = exportcsv.read_words_list()
    max_index = exportcsv.get_total_lines(sheet)
    rows = list(sheet.rows)
    
    for step_index in range(int(total_words_toask)):
        random_index = int(random.uniform(1, max_index))
        row = rows[random_index]
        results.append(do_step(step_index, (row[0].value, row[1].value)))

def calc_stats():
    """
    calculates and prints ratio
    """
    if len(results) > 0:
        success_ratio = results.count(True)/len(results)

        if flag_do_write: exportcsv.write_stats(number_words, success_ratio)

        print('Success ratio: %s' % success_ratio)

def ask_word(word_translate):
    """
    prints and gets input for single word
    """

    message = input("Translate (%s): %s \n" % (lang_from.upper(), word_translate))
    return message

def read_single_word(text_to_read):
    """
    voiceover for single word
    using global 'lang_to' for lang selection
    """

    tmp_file_name = 'tmp_%s.mp3' % str(random.uniform(1, 10e5)).replace('.', '')
    tts = gTTS(text=text_to_read, lang=lang_to)
    tts.save(tmp_file_name)

    music = pyglet.media.load(tmp_file_name, streaming=False)
    music.play()

    sleep(music.duration)
    os.remove(tmp_file_name)

def do_step(step_index, word_pair):
    """
    does actions for reading and saking one word pair
    """

    print(step_index)
    if flag_do_sound: read_single_word(word_pair[1])
    res = ask_word(word_pair[0])
    step_result = False
    if res.lower() == word_pair[1].lower():
        print('Correct! \n')
        step_result = True
    else:
        print('Wrong, correct is: %s' % word_pair[1])
        print('\n')

    return step_result

def parse_cli_args():
    DO_SILENT = '-silent'
    DO_SKIP_WRITE = '-test'
    DO_NUMBER = '-n'

    global flag_do_sound
    global flag_do_write
    global number_words

    args = sys.argv
    usedargs = args[1:]

    for argument_index, item in enumerate(usedargs):
        if(item == DO_SILENT): 
             flag_do_sound = False

        if(item == DO_SKIP_WRITE): 
             flag_do_write = False

        if(argument_index <= len(usedargs) and item == DO_NUMBER): 
             number_words = usedargs[argument_index+1]

def init():
    parse_cli_args()
    global lang_from, lang_to
    lang_from, lang_to = exportcsv.read_language_pair()
    print(lang_from, ' -> ', lang_to)
    #ask_words_list(number_words)
    ask_random_words_list(number_words)
    calc_stats()

if __name__ == '__main__':
    try:
        init()
    except KeyboardInterrupt:
        print ('\n Closing')
        calc_stats()
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
