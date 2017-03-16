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

# TODOs:
#  - read langs from file
#  - write to excke file

# def print_words():
#     sh = exportcsv.read_words_list()
#     for i, row in enumerate(sh.rows):
#         if i == 0:
#             print(row[0].value, '      ', row[1].value)
#             print ('------------')
#         else:
#             print(' %s  -  %s' % (row[0].value, row[1].value))

def ask_words_list(limit=number_words):
    """
    iterates certain amount of word lines
    """

    start = 15
    sh = exportcsv.read_words_list()
    results = []
    for i, row in enumerate(sh.rows):
        if i > start and i <=limit + start:
            results.append(do_step(i, (row[0].value, row[1].value)))
    
    return results

def calc_stats(results_list):
    """
    calculates and prints ratio
    """

    ratio = results_list.count(True)/len(results_list)

    if flag_do_write: exportcsv.write_stats(number_words, ratio)

    print('Success ratio: %s', ratio)

def ask_word(word, lang='en'):
    """
    prints and gets input for single word
    """

    message = input("Translate (%s): %s \n" % (lang.upper(), word))
    return message

def read_single_word(text, lang='en'):
    """
    voise for single word
    """

    tmp_file_name = 'tmp_%s.mp3' % str(random.uniform(1, 10e5)).replace('.', '')
    tts = gTTS(text=text, lang=lang)
    tts.save(tmp_file_name)

    music = pyglet.media.load(tmp_file_name, streaming=False)
    music.play()

    sleep(music.duration)
    os.remove(tmp_file_name)

def do_step(index, word_pair):
    """
    does actions for reading and saking one word pair
    """

    print(index)
    if flag_do_sound: read_single_word(word_pair[1], lang)
    res = ask_word(word_pair[0], lang)
    result = False
    if res == word_pair[1]:
        print('Correct! \n')
        result = True
    else:
        print('Wrong, correct is: %s' % word_pair[1])
        print('\n')

    return result

def parse_args():
    DO_SILENT = '-silent'
    DO_SKIP_WRITE = '-test'
    DO_NUMBER = '-n'
    
    args = sys.argv
    usedargs = args[1:]

    for index, item in enumerate(usedargs):
        print(len(usedargs), index, item == DO_NUMBER, int(usedargs[index+1]))
        # if(item == DO_SILENT): 
        #      global flag_do_sound
        #      flag_do_sound = False

        # if(item == DO_SKIP_WRITE): 
        #      global flag_do_write
        #      flag_do_write = False

        if(index <= len(usedargs) and item == DO_NUMBER): 
             global number_words
             number_words = usedargs[index+1]
    
    print(flag_do_sound, flag_do_write, number_words)

def init():
    parse_args()
    read_language_pair()
    #calc_stats(ask_words_list(number_words))

init()
