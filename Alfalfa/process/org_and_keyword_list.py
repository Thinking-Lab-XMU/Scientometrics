# -*- coding:utf-8 -*-
# @Time    : 2020/9/7 20:48
# @Author  : Heying Zhu

'''
Cleaning data with institutional thesaurus and keyword Thesaurus(Provided by experts)
'''


import pandas as pd

# Extracting key words and merging synonyms from keyword Thesaurus
def extract_keyword():
    path = "D:/data/thesaurus/keyword.xlsx"
    with open(path, "rb") as f:
        data = pd.read_excel(f, header=None)
    keyword_list = []
    for index, row in data.iterrows():
        if row[0].startswith("**") and row[0][2:] not in keyword_list:
            keyword_list.append(row[0][2:])
        elif row[0].startswith("100 1 ^") and row[0][7:-1] not in keyword_list:
            keyword_list.append(row[0][7:-1])
    return keyword_list


# extract_org
def extract_org():
    path = "D:/data/thesaurus/org.THE"
    with open(path) as f:
        results = f.read().split("**")

    # 对于每一个机构
    org_alias_dict = {}   # 机构别名参照表
    for result in results:
        if result != "":
            name_list = result.split("\n100 1 ^")
            templist = []
            for i in range(1, len(name_list)):
                if i == len(name_list)-1:
                    templist.append(name_list[i][:-2])
                else:
                    templist.append(name_list[i][:-1])
            org_alias_dict[name_list[0]] = templist

    return org_alias_dict


# According to the organization alias dictionary, the update statement is generated
def generate_update_sql(org_alias_dict):
    update_sqls = ""
    for key, value in org_alias_dict.items():
        conditions = "org_new like \"%" + key + "%\" "
        for item in value :
            conditions = conditions + "or org_new like \"%" + item + "%\" "
        sql = "update papar_country set org_new=\"" + key + "\" where " + conditions + ";"
        update_sqls = update_sqls + sql
    print(update_sqls)


# General vocabulary
def extract_common_words():
    path = "D:/data/thesaurus/common_words.txt"
    with open(path, "r") as f:
        content = f.read()
    common_word = content.split("\n")
    return common_word





if __name__ == "__main__":
    org_alias_dict = extract_org()
    generate_update_sql(org_alias_dict)
    extract_keyword()

    extract_common_words()