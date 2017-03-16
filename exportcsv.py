import openpyxl
from time import gmtime, strftime

filename = 'words.xlsx'

def get_file_and_wb():
    wb = openpyxl.load_workbook(filename)    
    return wb

def read_language_pair ():
    sheet = get_file_and_wb().get_sheet_by_name('words')
    first_row = sheet[1]
    return first_row[0].value, first_row[1].value

def read_words_list (from_pos=0, to_pos=100):
    sheet = get_file_and_wb().get_sheet_by_name('words')
    return sheet

def write_stats (words_numer, ratio):
    wb = get_file_and_wb()
    sheet = wb.get_sheet_by_name('results')
    cut_time =  strftime("%A, %d %b %H:%M", gmtime())

    for i, row in enumerate(sheet.rows):
        index = i + 1
        if sheet.cell(column=2, row=index).value:
            pass

    sheet.cell(column=1, row=(index+1)).value = cut_time
    sheet.cell(column=2, row=(index+1)).value = words_numer
    sheet.cell(column=3, row=(index+1)).value = ratio
    wb.save(filename = filename)
