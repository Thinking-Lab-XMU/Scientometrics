#-*- coding:utf-8 -*-
# @Time    : 2020/08/20 15:29
# @Author  : Heying Zhu

'''
Analyze the SCI data (TXT format) downloaded from web of science and save it as a local CSV file for subsequent processing.
The data related to Lake Lucerne in Switzerland are excluded.
It is mainly the data of Alfalfa papers.
'''

import os
import re
import pandas as pd
import datetime

# Fields included(54个)
keys = {'EI', 'CL', 'BE', 'UT', 'VL', 'AB', 'X4', 'DI', 'EA', 'SP', 'OI', 'SE', 'Y4', 'PM', 'Z9', 'CY', 'ZS', 'Z1',
        'PT', 'Z2', 'ZB', 'SN', 'BN', 'BP', 'TI', 'Z4', 'PN', 'AR', 'PY', 'SO', 'X1', 'TC', 'AK', 'Z8', 'GP', 'AU',
        'HO', 'AE', 'RI', 'IS', 'BA', 'FT', 'D2', 'DN', 'PD', 'SU', 'Y1', 'S1', 'ZR', 'EP', 'CT', 'SI', 'CA', 'MA'}


# Fields contained in all TXT documents
contain_keys = set([])

# Fields not required
exclude_keys = ['FT', 'VR', 'ER', 'EF']

# Fields that do not need to replace "\n"
no_replace_keys = ['AU', 'AF', 'C1', 'CR']

# txt to csv
def process_data(load_path, save_path):
    final_data = pd.DataFrame()
    # Traverse all the txt files in the directory
    for file in os.listdir(load_path):
        print("Current processing TXT file:", file)
        # 读取文件内容
        line_file = open(load_path + file, 'r', encoding='UTF-8-sig').read()
        records = re.split("\nER", line_file)
        records = records[:-1]

        for record in records:
            values = re.split("([\n](?![^A-Za-z]))", record)    # Divide a record into multiple lines
            one_dict = {}
            for value in values:
                if value[:2] == "FN" or value == "\n" or value[:2] in exclude_keys:
                    continue
                key = value[:2]
                if key not in contain_keys and key not in exclude_keys:
                    print(key)
                    print(file)
                    contain_keys.add(key)
                if key not in no_replace_keys:
                    one_dict[key] = value[3:].replace("\n   "," ")
                else:
                    one_dict[key] = value[3:]
            final_data = final_data.append([one_dict], ignore_index=True)

    # All processing is complete
    final_data.to_csv(save_path + "all.csv", index=False)
    print("All processing is complete!")


# Data cleaning: sifting out the relevant data of Lucerne Lake in Switzerland
def data_clean(save_path):
    # Title of error data(Expert judgment)
    title_list = ["Relay crops: a source of nutritional forage",
                  "The importance of water for forage crops in major areas of production",
                  "Traits related to differences in function among three arbuscular mycorrhizal fungi"]
    check_keys = ['AB', 'AK', 'SU', 'TI', 'TS', 'DE', 'ID', 'KP']
    all_data = pd.read_csv(save_path + "all.csv")
    clean_after = pd.DataFrame()
    screen_data = pd.DataFrame()    # Data on Lake Lucerne, Switzerland

    # Traverse all data
    flag = -1
    flag_two = False
    for index, row in all_data.iterrows():
        if index%100 == 0 and index != 0:
            print("It has been processed ", index, "data！", datetime.datetime.now().strftime('%Y.%m.%d-%H:%M:%S'))
        # Check the field to be checked to determine whether there is one of the three keywords
        for item in check_keys:
            if item in row and not pd.isnull(row[item]) and (row[item].find('Switzerland') >= 0 or
                                                             row[item].find('Lake Lucerne') >= 0 or
                                                             row[item].find('Lakes Lucerne') >= 0):
                flag = index
        if row['TI'] in title_list:
            flag_two = True
        if flag == index and not flag_two:
            screen_data = screen_data.append(row, ignore_index=True)
        else:
            clean_after = clean_after.append(row, ignore_index=True)
            if flag_two:
                flag_two = False

    screen_data.to_csv(save_path + "Lake Lucerne.csv", index=False)
    clean_after.to_csv(save_path + "clean_after.csv", index=False)



if __name__ == '__main__':
    # The root directory of the txt data store
    load_path = "D:/data/txt/"
    # Target CSV save directory
    save_path = "D:/code/data/"

    # Save all TXT data as CSV
    process_data(load_path, save_path)

    # The relevant data of lucerne Lake in Switzerland were screened out
    data_clean(save_path)

    print("The end！")
