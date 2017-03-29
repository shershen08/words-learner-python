import exportcsv
import argparse

import random
import os
import sys
import glob
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
used_indices = []
results = []
sound_tmp_dir = 'tmp'
sound_vocabulary_filename = 'vocabulary.mp3'

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    # Print New Line on Complete
    if iteration == total: 
        print()

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
    mashup = AudioSegment.empty()
    ding = AudioSegment.from_mp3("ding_sound.mp3")
    less_loud_ding = ding - 20
    half_second_of_silence = AudioSegment.silent(duration=500)

    sheet = exportcsv.read_words_list()
    max_index = exportcsv.get_total_lines(sheet)
    rows = list(sheet.rows)
    rows.pop(0)
    
    create_dir_if_needed()


    i = 0
    l = len(rows)
    # Initial call to print 0% progress
    printProgressBar(i, l, prefix = 'Progress:', suffix = 'Complete', length = 50)

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
        printProgressBar(i, l, prefix = 'Progress:', suffix = 'Complete', length = 50)

    mashup.export(sound_vocabulary_filename, format="mp3")
    clear_tmp_dir()
    print('generated vocabulary file')

def ask_word(word_translate):
    """
    prints and gets input for single word
    """
    message = input("Translate (%s): %s \n" % (lang_from.upper(), word_translate))
    return message

def check_file_exists(name):
    return os.path.exists(name)

def clear_tmp_dir():
    path = '%s/*' % sound_tmp_dir
    files = glob.glob(path)
    for f in files:
        os.remove(f)

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
    parser = argparse.ArgumentParser(description='Words reading and checking')
    parser.add_argument('-silent', action='store_false', help='Skip word voiceover while iterating ')
    parser.add_argument('-test', action='store_false', help='Do not save quiz results to file')
    parser.add_argument('-n', help='Number of words to ask')
    parser.add_argument('-r', action='store_false', help='Reverse source file collumns usage')
    parser.add_argument('-f', help='Filename to process (default: words.xslx)')
    parser.add_argument('-vocfile', action='store_true', help='Generate a file with all words pronounced')
    args = vars(parser.parse_args())
    numer_words = 10

    if (args['n']):
        numer_words = args['n']

    if (args['f'] and check_file_exists(args['f'])):
        exportcsv.set_filename(args['f'])

    return args['test'], args['r'], args['vocfile'], args['silent'], numer_words

def init():
    global flag_do_sound, flag_do_write, flag_do_vocfile, number_words
    flag_do_write, flag_reverse, flag_do_vocfile, flag_do_sound, number_words = parse_cli_args()

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
        clear_tmp_dir()

if __name__ == '__main__':
    try:
        init()
    except KeyboardInterrupt:
        print ('\n Closing')
        if(flag_do_vocfile is False):
            calc_stats()
            clear_tmp_dir()
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
