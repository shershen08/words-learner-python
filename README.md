
## Python foreign words learner

Reads words from the file, then produces the sound of the word and its translation in onle language, later checks the correctness of your typing in console for this word translation . Later calculated the stats and saves to the file.

Can be used with any two pairs of languages, say French -> German.

### Usage

Install dependances

Run: `python learner.py [OPTIONS]`

Command line parameters available:

 - `-n [NUMBER]` how many words to ask in one run, defaults to 10; for example `python learner.py -n 15`;
 - `-test` to skip writing the results to Excel file;
 - `-silent` to skipe workd voiceover while iterating;

### Data file structure

Excel file is stored in the same folder and is used to store the words that need to be checked (can be added by hand on Sheet 1) and the results of the tests (on Sheet 2).

Excel file filename: `words.xlsx`

Sheet 1: `words`
Columns: language names; in this demo case it is `en` and `it`.
First column should contain the language known to the user, while the second one the language being learned.

Sheet 2: `results`
Columns: Date, Words tested, Ratio

### Dependances

Project uses Python3. So if you have Python v.2 as a default in your setup you need to use `vitrualenv` and/or run the project with `python3 learner.py`

Python libs:
 - exportcsv
 - gtts
 - pyglet

Media library (for playing sound files):
 - AVbin [download](https://avbin.github.io/AVbin/Download.html)

 ### Description in jupyter

 To run use `jupyter notebook` when in the project folder. And the open a `word_reader.ipynb` file.

 ### License

 MIT