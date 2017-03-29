import exportcsv

import glob
import argparse
import os

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

def create_dir_if_needed(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

def clear_tmp_dir(sound_dir):
    path = '%s/*' % sound_dir
    files = glob.glob(path)
    for f in files:
        os.remove(f)

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

    if (args['f'] and  os.path.exists(args['f'])):
        exportcsv.set_filename(args['f'])

    return args['test'], args['r'], args['vocfile'], args['silent'], numer_words