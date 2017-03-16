import openpyxl

def get_file_and_wb():
    filename = 'words.xlsx';
    wb = openpyxl.load_workbook(filename)    
    return wb

def read_language_pair ():
    sheet = get_file_and_wb().get_sheet_by_name('words')
    first_row = sheet.rows[0]
    return first_row[0].value, first_row[1].value

def read_words_list (from_pos=0, to_pos=100):
    sheet = get_file_and_wb().get_sheet_by_name('words')
    return sheet

def write_stats (words_numer, ratio):
    sheet = get_file_and_wb().get_sheet_by_name('results')
    return sheet

# get_column_letter(sheet.get_highest_column())
# 'C'
# >>> column_index_from_string('A')
# 1
# >>> column_index_from_string('AA')