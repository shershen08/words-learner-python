import exportcsv


import random
import os
import sys
from time import sleep

from pydub import AudioSegment
from gtts import gTTS
import pyglet

pyglet.lib.load_library('avbin')
pyglet.have_avbin=True

# set global flags
lang_from = 'en'
lang_to = 'en'
flag_do_sound = True
flag_do_write = True
flag_do_vocfile = False
number_words = 10

#global var 
results = []
sound_tmp_dir = 'tmp'
sound_vocabulary_filename = 'vocabulary.mp3'

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


def generate_sound_file(text_to_read, lang_to_use):
    """
    creates a mp3 file with read word
    """
    tmp_file_name = '%s/tmp_%s.mp3' % (sound_tmp_dir, str(random.uniform(1, 10e6)).replace('.', ''))
    tts = gTTS(text=text_to_read, lang=lang_to_use)
    tts.save(tmp_file_name)
    return tmp_file_name

def generate_voc_file():
    """
    iterates words and concatenates them with separator in between
    """
    mashup = AudioSegment.empty()
    ding = AudioSegment.from_mp3("ding_sound.mp3")

    sheet = exportcsv.read_words_list()
    max_index = exportcsv.get_total_lines(sheet)
    rows = list(sheet.rows)

    create_dir_if_needed()

    for row in rows:
        word_file_1 = generate_sound_file(row[0].value, lang_to)
        word_file_2 = generate_sound_file(row[1].value, lang_from)
        word1 = AudioSegment.from_mp3(word_file_1)
        word2 = AudioSegment.from_mp3(word_file_2)
        mashup = mashup + word1 + word2 + ding
        os.remove(word1)
        os.remove(word2)
        
    mashup.export(sound_vocabulary_filename, format="mp3")
    print('generated vocabulary file')

def ask_word(word_translate):
    """
    prints and gets input for single word
    """

    message = input("Translate (%s): %s \n" % (lang_from.upper(), word_translate))
    return message

def create_dir_if_needed():
    if not os.path.exists(sound_tmp_dir):
        os.makedirs(sound_tmp_dir)

def read_single_word(text_to_read):
    """
    voiceover for single word
    using global 'lang_to' for lang selection
    """
    create_dir_if_needed()
    tmp_file_name = generate_sound_file(text_to_read, lang_to)

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
    DO_VOCFILE = '-vocfile'

    global flag_do_sound
    global flag_do_write
    global flag_do_vocfile
    global number_words

    args = sys.argv
    usedargs = args[1:]

    for argument_index, item in enumerate(usedargs):
        if(item == DO_SILENT): 
             flag_do_sound = False

        if(item == DO_SKIP_WRITE): 
             flag_do_write = False
        
        if(item == DO_VOCFILE): 
             flag_do_vocfile = True

        if(argument_index <= len(usedargs) and item == DO_NUMBER): 
             number_words = usedargs[argument_index+1]

def init():
    parse_cli_args()
    global lang_from, lang_to
    lang_from, lang_to = exportcsv.read_language_pair()
    print(lang_from, ' -> ', lang_to)
    #ask_words_list(number_words)

    if(flag_do_vocfile is True):
        generate_voc_file()
    else:
        ask_random_words_list(number_words)
        calc_stats()

if __name__ == '__main__':
    try:
        init()
    except KeyboardInterrupt:
        print ('\n Closing')
        if(flag_do_vocfile is False):
            calc_stats()

        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
