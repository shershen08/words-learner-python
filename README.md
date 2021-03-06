
## Python foreign words learner 🇬🇧 🇫🇷 🇧🇷 

Reads words from the file, then produces the sound of the word and its translation in one language, later checks the correctness of your typing in console for this word's translation. Later the calculated stats are saved to the file.

Can be used with any two pairs of languages, say French -> German. List of supported languages depends on the gtts library, [the full list see here](https://pypi.python.org/pypi/gTTS)

### Usage

 1. Install dependances

 2. Run: `python learner.py [OPTIONS]`

⚙ Command line parameters available:

 - `-h` show help options;
 - `-n [NUMBER]` how many words to ask in one run, defaults to 10; for example `python learner.py -n 15`;
 - `-test` to skip writing the results to Excel file;
 <!--- `-r` reverse Excel file collumns;-->
 - `-silent` to skip word voiceover while iterating;
 - `-vocfile` skip the test and generate a single file with all words pairs;
 - `-f [PATH_AND_FILENAME]` set source filename different from 'words.xlsx';

### Data file structure

📖 Excel file is stored in the same folder and is used to store the words that need to be checked (can be added by hand on Sheet 1) and the results of the tests (on Sheet 2).

Default excel file filename - `words.xlsx` (can be changed with `-f` option)

**Sheet 1**: `words`

Columns: language names; in this demo case it is `en` and `it` which means English and Italian.

First column should contain the language known to the user, while the second one the language being learned.

**Sheet 2**: `results`

Columns: Date, Words tested, Ratio

Outputs the results of the test 📊.

### Dependances

Project uses Python3. So if you have Python v.2 as a default in your setup (MacOS for example) you need to use `vitrualenv` and/or run the project with `python3 learner.py`

Python libs:
 - exportcsv
 - gtts
 - pyglet
 - pydub

Media library (for playing sound files):
 - AVbin [download](https://avbin.github.io/AVbin/Download.html)

 <!--### Description in jupyter

 To run use `jupyter notebook` when in the project folder. And the open a `word_reader.ipynb` file.-->

 ### Vocabulary reading 📢
 
 Now you can generate one file to repeat all your vocabulary pairs. May be handy to dowonload and listen latr on you mobile device. Use `-vocfile` option for that. Sample output you can see here: [italian - english words reading .mp3 file, 2Mb](http://picosong.com/pAB2)

 For this feature the pydub is used that relies on ffmpeg. Installation [pydub tips here](https://github.com/jiaaro/pydub#installation).

 The "ding" sound is by [Kastenfrosch](https://www.freesound.org/people/Kastenfrosch/sounds/162464/).
 
 
 ### TODOs
 
 1. add frontend to upload/download files so that the app could run on heroku or GCE
 2. add non-techy description / images
 3. option to parse translate.google.com excel file format
 4. add option to reverse languages 

 ### License

 MIT
