import pandas as pd
import time
import json
from collections import ChainMap
from numpy import *


with open('config.json') as json_file:
    config_efficiency_class = ChainMap(json.load(json_file))
    # print(config_efficiency_class)

a = config_efficiency_class['A']
b = config_efficiency_class['B']
c = config_efficiency_class['C']
d = config_efficiency_class['D']
e = config_efficiency_class['E']
f = config_efficiency_class['F']
g = config_efficiency_class['G']

path_database = None
if a and b and c and d:
    path_database = 'Archiv\A_B_C_D'
if e:
    path_database = 'Archiv\E'
if f:
    path_database = 'Archiv\F'
if g:
    path_database = 'Archiv\G'
print(path_database)


def start_classify(a, b, c, d, e, f, g):
    ''' ------------------- Read Excel File ----------------------- '''
    df = None
    if a and b and c and d:
        df = pd.read_excel(path_database + '\data_base_all_appliances_A_B_C_D_.xlsx')
    if e:
        df = pd.read_excel(path_database + '\data_base_all_appliances_E_.xlsx')
    if f:
        df = pd.read_excel(path_database + '\data_base_all_appliances_F_.xlsx')
    if g:
        df = pd.read_excel(path_database + '\data_base_all_appliances_G_.xlsx')

    # df = pd.read_excel('data_base_all_appliances.xlsx')
    excel_file = [list(row) for row in df.values]
    excel_file.insert(0, df.columns.to_list())

    element = []
    element_total1 = []
    element_total2 = []
    element_total3 = []

    ''' ------------------- columns, sorting 1 ------------------------- '''
    count = 0
    cache1 = []
    while count < len(excel_file):
        count_row = 0
        for row in excel_file[count]:
            if count_row == 23 and row == "Defrosting type":
                for row1 in excel_file[count]:
                    cache1.append(row1)
                element.append(cache1[25])
                element.append(cache1[26])
                element.append(cache1[27])
                element.append(cache1[28])
                element.append(cache1[23])
                element.append(cache1[24])
                nurmber1 = 29
                while nurmber1 < len(cache1):
                    element.append(cache1[nurmber1])
                    nurmber1 = nurmber1 + 1
                cache1 = []
                break
            if count_row == 27 and row == "manual defrost":
                element.insert(27, '')
                element.append(row)
            if count_row == 27 and row == "Freezing capacity":
                element.insert(27, '')
                element.insert(28, '')
                element.insert(29, '')
                element.insert(30, '')
                element.insert(31, '')
                element.insert(32, '')
                element.insert(33, '')
                element.append(row)
            if count_row == 32 and row == "Defrosting type":
                for row1 in excel_file[count]:
                    cache1.append(row1)
                element.append(cache1[34])
                element.append(cache1[35])
                element.append(cache1[36])
                element.append(cache1[37])
                element.append(cache1[32])
                element.append(cache1[33])
                nurmber1 = 38
                while nurmber1 > len(cache1):
                    element.append(cache1[nurmber1])
                    nurmber1 = nurmber1 + 1
                cache1 = []
                break
            if count_row == 41 and row == "Defrosting type":
                for row1 in excel_file[count]:
                    cache1.append(row1)
                element.append(cache1[43])
                element.append(cache1[44])
                element.append(cache1[45])
                element.append(cache1[46])
                element.append(cache1[41])
                element.append(cache1[42])
                nurmber1 = 47
                while nurmber1 > len(cache1):
                    element.append(cache1[nurmber1])
                    nurmber1 = nurmber1 + 1
                cache1 = []
                break
            else:
                element.append(row)
            count_row = count_row + 1
        element_total1.append(element)
        element = []
        count = count + 1

    ''' ------------------- columns, sorting 2 ------------------------- '''
    element2 = []
    count2 = 0
    while count2 < len(element_total1):
        count_row = 0
        for row in element_total1[count2]:
            if count_row == 22:
                # print("row == 22")
                row = row.replace(' ', '')
            if count_row == 24:
                # print("row == 24")
                row = row.replace('\n', '')
            if count_row == 29 and row != "Recommended temperature setting for optimised food storage":
                element2.insert(29, '')
                element2.insert(30, '')
                element2.insert(31, '')
                element2.insert(32, '')
                element2.insert(33, '')
                element2.insert(34, '')
                element2.insert(35, '')
                element2.insert(36, '')
                element2.append(row)
            else:
                element2.append(row)
            count_row = count_row + 1
        element_total2.append(element2)
        element2 = []
        count2 = count2 + 1

    ''' ------------------- columns, sorting 3 ------------------------- '''
    element3 = []
    count3 = 0
    cache3 = []
    while count3 < len(element_total2):
        count_row = 0
        for row in element_total2[count3]:
            if count_row == 41:
                if row == '-':
                    row = row.replace('-', '')
            if count_row == 50:
                if row == '-':
                    row = row.replace('-', '')

            if count_row == 58 and row == "Defrosting type":
                for row1 in element_total2[count3]:
                    cache3.append(row1)
                element3.append(cache3[60])
                element3.append(cache3[61])
                element3.append(cache3[62])
                element3.append(cache3[63])
                element3.append(cache3[58])
                element3.append(cache3[59])
                nurmber1 = 64
                while nurmber1 < len(cache3):
                    element.append(cache3[nurmber1])
                    nurmber1 = nurmber1 + 1
                break
            # if count_row == 59:
            #     if row == '-':
            #         row = row.replace('-', '')
            else:
                element3.append(row)
            count_row = count_row + 1
        element_total3.append(element3)
        element3 = []
        count3 = count3 + 1

    ''' ------------------------ DataFrame --------------------------------------- '''

    element_total = pd.DataFrame(element_total3)
    ''' 0,1,2,3 ... '''

    element_total[12] = element_total[12].str.replace('dB', '', regex=True)
    element_total[12] = element_total[12].str.replace('(', '', regex=True)
    element_total[12] = element_total[12].str.replace('A', '', regex=True)
    element_total[12] = element_total[12].str.replace(')', '', regex=True)
    element_total[12] = element_total[12].str.replace(' re 1 pW', '', regex=True)
    element_total[12] = element_total[12].str.replace(' ', '', regex=True)
    element_total[12] = element_total[12].str.replace(',', '.', regex=True)
    element_total[12] = pd.to_numeric(element_total[12], downcast="float")

    element_total[13] = element_total[13].str.replace('(A - D)', '', regex=True)
    element_total[13] = element_total[13].str.replace('(', '', regex=True)
    element_total[13] = element_total[13].str.replace(')', '', regex=True)

    element_total[14] = element_total[14].str.replace(' ', '', regex=True)
    element_total[14] = element_total[14].str.replace('kWh/annum', '', regex=True)
    element_total[14] = element_total[14].str.replace(',', '.', regex=True)
    element_total[14] = pd.to_numeric(element_total[14], downcast="float")

    colum = 10
    element_total[colum] = element_total[colum].str.replace('dm³ or l', '', regex=True)
    element_total[colum] = element_total[colum].str.replace(' ', '', regex=True)
    element_total[colum] = element_total[colum].str.replace('-', '', regex=True)
    element_total[colum] = element_total[colum].str.replace('\n', '', regex=True)
    element_total[colum] = element_total[colum].str.replace(',', '.', regex=True)
    element_total[colum] = pd.to_numeric(element_total[colum], downcast="float")



    ''' COMPARTMENT #2: row = 37 '''

    ''' Recommended temperature setting for optimised food storage: 41 '''
    element_total[41] = element_total[41].str.replace('°C', '', regex=True)

    ''' COMPARTMENT #3: row = 46 '''


    ''' Recommended temperature setting for optimised food storage: 49 '''
    element_total[50] = element_total[50].str.replace('\n', '', regex=True)
    element_total[50] = element_total[50].str.replace('°C', '', regex=True)

    ''' Recommended temperature setting for optimised food storage: 59 '''
    element_total[59] = element_total[59].str.replace('\n', '', regex=True)
    element_total[59] = element_total[59].str.replace('°C', '', regex=True)

    def string_to_float_dm_or_l(colum):
        element_total[colum] = element_total[colum].str.replace('dm³ or l', '', regex=True)
        element_total[colum] = element_total[colum].str.replace('°C', '', regex=True)
        element_total[colum] = element_total[colum].str.replace(' ', '', regex=True)
        element_total[colum] = element_total[colum].str.replace('-', '', regex=True)
        element_total[colum] = element_total[colum].str.replace('\n', '', regex=True)
        element_total[colum] = element_total[colum].str.replace(',', '.', regex=True)
        element_total[colum] = pd.to_numeric(element_total[colum], downcast="float")
        return

    ''' dm³ or l '''
    string_to_float_dm_or_l(22)
    string_to_float_dm_or_l(39)
    string_to_float_dm_or_l(48)
    string_to_float_dm_or_l(57)

    def string_to_float_C(colum):
        element_total[colum] = element_total[colum].str.replace(' ', '', regex=True)
        element_total[colum] = element_total[colum].str.replace('°C', '', regex=True)
        element_total[colum] = element_total[colum].str.replace('-°C', '', regex=True)
        element_total[41] = element_total[41].str.replace('Kg/24h', '', regex=True)
        for row in element_total[colum]:
            if row == "-":
                element_total[colum] = element_total[colum].replace('-', '')
        element_total[colum] = element_total[colum].str.replace(',', '.', regex=True)
        element_total[colum] = pd.to_numeric(element_total[colum], downcast="float")
        return

    ''' °C '''
    string_to_float_C(16)
    string_to_float_C(17)
    string_to_float_C(24)
    string_to_float_C(30)
    string_to_float_C(34)
    string_to_float_C(50)
    string_to_float_C(59)

    def string_to_float_Kg_24h(colum):
        element_total[colum] = element_total[colum].str.replace('-', '', regex=True)
        element_total[colum] = element_total[colum].str.replace('\n', '', regex=True)
        element_total[colum] = element_total[colum].str.replace('Kg/24h', '', regex=True)
        element_total[colum] = element_total[colum].str.replace('Kg/24h', '', regex=True)
        element_total[colum] = element_total[colum].str.replace('°C', '', regex=True)
        element_total[colum] = element_total[colum].str.replace(' ', '', regex=True)
        element_total[colum] = element_total[colum].str.replace(',', '.', regex=True)
        element_total[colum] = pd.to_numeric(element_total[colum], downcast="float")
        return

    ''' Kg/24h '''
    string_to_float_Kg_24h(26)
    string_to_float_Kg_24h(32)
    string_to_float_Kg_24h(36)
    string_to_float_Kg_24h(43)
    string_to_float_Kg_24h(52)
    string_to_float_Kg_24h(61)

    ''' ------------------------- header ----------------------------------------------'''
    headline = []
    for row in range(99):
        headline.append(str(row))
        # print(headline)

    ''' ----------------------- local time -------------------------------------------- '''
    print("local time")
    t = time.localtime()
    date_now = str(t.tm_year) + str(t.tm_mon) + str(t.tm_mday) + str(t.tm_hour)
    ''' ---------------------- Save Excel File ------------------------------------------------'''
    print("wait until excel file is completely saving ...")


    efficiency_class_output = '_'
    for efficiency_class, value in config_efficiency_class.items():
        # print(efficiency_class, value)
        if value:
            efficiency_class_output = efficiency_class_output + efficiency_class
            efficiency_class_output = efficiency_class_output + '_'

    print(efficiency_class_output)
    file_name_excel = (path_database + '\data_base_all_classify' + efficiency_class_output + date_now + '.xlsx')
    data_base_ref_appliances = pd.DataFrame(element_total)
    # data_base_ref_appliances.to_excel(file_name_excel, index=False, header=headline)
    data_base_ref_appliances.to_excel(file_name_excel, index=False, header=False)
    print("end")


''' test manuel: start_classify '''
# start_classify(a, b, c, d, e, f, g)
