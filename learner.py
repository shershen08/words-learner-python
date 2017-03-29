import exportcsv
import utils

import random
import os
import sys

from time import sleep, gmtime, strftime

from pydub import AudioSegment
from gtts import gTTS
import pyglet

pyglet.lib.load_library('avbin')
pyglet.have_avbin=True

# set global flags
lang_from, lang_to = 'en', 'en'
flag_do_sound, flag_do_write, flag_do_vocfile  = True, True, False

#global var 
number_words = 10
used_indices = []
results = []
sound_tmp_dir = 'tmp'
sound_vocabulary_filename = 'vocabulary'

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

def get_random_index(max_av_index):
    """
    maintains a list of already used indexes and generates always a unique one
    """
    global used_indices
    def generate_ind():
        return int(random.uniform(1, max_av_index))
    
    #get unique one
    selected_ind = generate_ind()
    while (selected_ind in used_indices or selected_ind == 1):
        selected_ind =  generate_ind()
    
    used_indices.append(selected_ind)
    return selected_ind

def ask_random_words_list(total_words_toask=number_words):
    """
    checks words from random parts of the list
    """
    global results

    sheet = exportcsv.read_words_list()
    max_index = exportcsv.get_total_lines(sheet)
    rows = list(sheet.rows)

    for step_index in range(int(total_words_toask)):
        random_index = get_random_index(max_index)
        row = rows[random_index-1]
        results.append(do_step(step_index, (row[0].value, row[1].value)))

def calc_stats():
    """
    calculates and prints ratio
    """
    if len(results) > 0:
        success_ratio = results.count(True)/len(results)

        if flag_do_write:
            exportcsv.write_stats(number_words, success_ratio)

        print('Success ratio: %s' % success_ratio)


def generate_sound_file(text_to_read, lang_to_use):
    """
    creates a mp3 file with read word
    """
    tmp_file_name = '%s/tmp_%s.mp3' % (sound_tmp_dir, str(random.uniform(1, 10e6)).replace('.', ''))

    try:
        tts = gTTS(text=text_to_read, lang=lang_to_use)
        tts.save(tmp_file_name)
        return tmp_file_name
    except:
        print('Error: selected language \'%s\' is not supported by the Google Text to Speech API, https://pypi.python.org/pypi/gTTS' % lang_to_use)
        sys.exit(0)

def generate_voc_file():
    """
    iterates words and concatenates them with separator in between
    """
    sheet = exportcsv.read_words_list()
    max_index = exportcsv.get_total_lines(sheet)
    rows = list(sheet.rows)
    rows.pop(0)
    
    utils.create_dir_if_needed(sound_tmp_dir)

    mashup = iterate_rows(rows)

    file_name = '%s %s to %s from %s.mp3' % (sound_vocabulary_filename, lang_to.upper(), lang_from.upper(), strftime("%d-%b-%Y %H:%M", gmtime()), )

    mashup.export(file_name , format="mp3")
    utils.clear_tmp_dir(sound_tmp_dir)
    print('Generated vocabulary file: %s' % file_name)

def iterate_rows(rows):
    mashup = AudioSegment.empty()
    ding = AudioSegment.from_mp3("ding_sound.mp3")
    less_loud_ding = ding - 20
    half_second_of_silence = AudioSegment.silent(duration=500)
    
    i = 0
    l = len(rows)
    # Initial call to print 0% progress
    utils.printProgressBar(i, l, prefix = 'Progress:', suffix = 'Complete', length = 50)

    for row in rows:
        word_file_1 = generate_sound_file(row[0].value, lang_from)
        word_file_2 = generate_sound_file(row[1].value, lang_to)
        word1 = AudioSegment.from_mp3(word_file_1)
        word2 = AudioSegment.from_mp3(word_file_2)
        #first - unknown lang, second - unknown lang
        mashup = mashup + word2 + half_second_of_silence + word1 + less_loud_ding
        os.remove(word_file_1)
        os.remove(word_file_2)
        i += 1
        utils.printProgressBar(i, l, prefix = 'Progress:', suffix = 'Complete', length = 50)

    return mashup

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
    utils.create_dir_if_needed(sound_tmp_dir)
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

def init():
    global flag_do_sound, flag_do_write, flag_do_vocfile, number_words
    flag_do_write, flag_reverse, flag_do_vocfile, flag_do_sound, number_words = utils.parse_cli_args()

    # TODO: implement Reverse option

    global lang_from, lang_to
    lang_from, lang_to = exportcsv.read_language_pair()
    print(lang_from, ' -> ', lang_to)
    #ask_words_list(number_words)

    if(flag_do_vocfile is True):
        generate_voc_file()
    else:
        ask_random_words_list(number_words)
        calc_stats()
        utils.clear_tmp_dir(sound_tmp_dir)

if __name__ == '__main__':
    try:
        init()
    except KeyboardInterrupt:
        print ('\n Closing')
        if(flag_do_vocfile is False):
            calc_stats()
            utils.clear_tmp_dir(sound_tmp_dir)
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
