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

def ask_words_list(limit=number_words):
    """
    iterates certain amount of word lines
    """

    start = 5
    sh = exportcsv.read_words_list()
    global results

    for i, row in enumerate(sh.rows):
        if i > start and i <=int(limit) + start:
            results.append(do_step(i, (row[0].value, row[1].value)))

def calc_stats():
    """
    calculates and prints ratio
    """
    
    ratio = results.count(True)/len(results)

    if flag_do_write: exportcsv.write_stats(number_words, ratio)

    print('Success ratio: %s' % ratio)

def ask_word(word, lang):
    """
    prints and gets input for single word
    """

    message = input("Translate (%s): %s \n" % (lang.upper(), word))
    return message

def read_single_word(text, lang):
    """
    voise for single word
    """

    tmp_file_name = 'tmp_%s.mp3' % str(random.uniform(1, 10e5)).replace('.', '')
    tts = gTTS(text=text, lang=lang_to)
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
    if flag_do_sound: read_single_word(word_pair[1], lang_from)
    res = ask_word(word_pair[0], lang_to)
    result = False
    if res.lower() == word_pair[1].lower():
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

    global flag_do_sound
    global flag_do_write
    global number_words

    args = sys.argv
    usedargs = args[1:]

    for index, item in enumerate(usedargs):
        if(item == DO_SILENT): 
             flag_do_sound = False

        if(item == DO_SKIP_WRITE): 
             flag_do_write = False

        if(index <= len(usedargs) and item == DO_NUMBER): 
             number_words = usedargs[index+1]

def init():
    parse_args()
    global lang_from, lang_to
    lang_from, lang_to = exportcsv.read_language_pair()
    print(lang_from, ' -> ', lang_to)
    ask_words_list(number_words)
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
