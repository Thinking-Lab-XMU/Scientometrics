"""
1. Papers are classified and screened according to intervention methods, and new txt is obtained according to the screening results
     a. [Thesis] wos data is merged into one excel, sorted by time (PD, EA) (nan put after), deduplicated by UT, deduplicated by TI and AB
     b. [Paper] Data and keywords are matched to obtain excel of clinical paper
     c. [Paper] The month field is added to the clinical paper table
     d. [Paper] According to UT, search for new papers and generate new txt
"""
import datetime
import os
import re
import pandas as pd
import numpy as np


def get_paper_excel(load_path, save_file):
    """
    Combine the wos data into an excel, sort by time (PD, EA) (nan put behind), deduplicate according to UT, deduplicate according to TI and AB
    :param load_path:  txt folder path
    :param save_file:  excel folder path
    :return: null
    """
    exclude_keys = ['FT', 'VR', 'ER', 'EF']

    final_data = pd.DataFrame()
    # 遍历目录底下的所有txt文件
    for file in os.listdir(load_path):
        print("The currently processed txt file：", file)
        # 读取文件内容
        line_file = open(load_path + file, 'r', encoding='UTF-8-sig').read()
        records = re.split("\nER", line_file)
        records = records[:-1]
        # 对于一条记录
        for record in records:
            record_key = re.split("([\n^][A-Z][A-Z0-9])", record)    # 将一条记录分成多行
            record_key.pop(0)
            rec = {}
            for (ke, el) in zip(record_key[::2], record_key[1::2]):
                re_key = ke.replace("\n", "")
                if re_key not in exclude_keys:
                    rec[re_key] = str(el).strip()
            final_data = final_data.append([rec], ignore_index=True)
    # 所有txt处理完成,去重并保存
    print('There are a total of' + str(len(final_data)) + 'data in txt')
    month_dict = {'JAN': 1, 'FEB': 2, 'MAR': 3, 'APR': 4, 'MAY': 5, 'JUN': 6, 'JUL': 7, 'AUG': 8, 'SEP': 9, 'OCT': 10,
                  'NOV': 11, 'DEC': 12}
    final_data['month'] = final_data.apply(lambda x: x['EA'].split(' ')[0].split('-')[0] if not pd.isnull(x['EA']) else (
        x['PD'].split(' ')[0].split('-')[0] if not pd.isnull(x['PD']) else None), axis=1)
    final_data['month'] = final_data['month'].apply(lambda x: month_dict[x] if month_dict.__contains__(x) else None)
    final_data.sort_values(by=['month'], inplace=True)  # nan默认在后面
    final_data.drop_duplicates(subset=['UT'], inplace=True)  # 默认保留前面那个
    print('after UT deduplication There are a total of' + str(len(final_data)) + 'data')
    final_data.drop_duplicates(subset=['TI', 'AB'], inplace=True)  # 默认保留前面那个
    print('after AB, TI deduplication There are a total of' + str(len(final_data)) + 'data')
    final_data.to_excel(save_file, index=False)


def get_dict(dict_file_name):
    """
    Get the intervention dictionary theme_word_dict
    Get Drug Dictionary drugs_dict
    :param dict_file_name:
    :return:
    """
    theme_words = pd.read_excel(dict_file_name)
    theme_word_dict = {}

    for column_name in list(theme_words.columns):
        result = []
        word_list = list(theme_words[column_name])
        for word in word_list:
            if word is np.nan:
                continue
            else:
                word_one_list = word.lower().strip().split("/")
                result.extend(word_one_list)
                word_others = []
                for word_one_one in word_one_list:
                    if word_one_one.find("#"):
                        word_others.append(word_one_one.replace("#", ' '))
                        word_others.append(word_one_one.replace("#", ' and '))
                result.extend(word_others)

        theme_word_dict[column_name] = result

    # TODO: Drug Dictionary（从上面抄的，改了一下，所以不要觉得奇怪）
    drugs_dict = {}
    column_name = '药物(Chemicals and Drugs)'
    word_list = list(theme_words[column_name])
    for word in word_list:
        if word is np.nan:
            continue
        else:
            word_one_list = word.lower().strip().split("/")
            drug_head = word_one_list[0]
            for drug_tail in word_one_list:
                drugs_dict[drug_tail] = drug_head
            word_others = []
            for word_one_one in word_one_list:
                if word_one_one.find("#"):
                    word_others.append(word_one_one.replace("#", ' '))
                    word_others.append(word_one_one.replace("#", ' and '))
            for drug_tail in word_others:
                drugs_dict[drug_tail] = drug_head

    return theme_word_dict, drugs_dict


def get_result_zero():
    public_result = 0
    scientific_result = 0
    intervention_result = 0

    return public_result, scientific_result, intervention_result


def get_type2(x, theme_word_dict, drugs_dict):
    """
    Filter data based on a column of the paper
    :param drugs_dict: Drug Dictionary
    :param x:
    :param theme_word_dict:Subject word dictionary
    :return:
    """
    # vaccine_list = ['vaccine', 'vaccines', 'covid-19 vaccine', 'viral vaccines']
    drug_name = []
    result_list = []

    public_result, scientific_result, intervention_result = get_result_zero()
    for word in theme_word_dict['中医药(Traditional Chinese Medicine)']:
        if x['AB'] is not np.nan and x['AB'].lower().find(word) != -1:
            public_result = 1
        if x['DE'] is not np.nan and x['DE'].lower().find(word) != -1:
            scientific_result = 1
        if x['TI'] is not np.nan and x['TI'].lower().find(word) != -1:
            intervention_result = 1
    if intervention_result == 1 or public_result == 1 or scientific_result == 1:
        result_list.append("中医药")

    public_result, scientific_result, intervention_result = get_result_zero()
    for word in theme_word_dict['AYUSH(Ayurveda, Yoga & Naturopathy, Unani, Siddha and Homoeopathy)']:
        if x['AB'] is not np.nan and x['AB'].lower().find(word) != -1:
            public_result = 1
        if x['DE'] is not np.nan and x['DE'].lower().find(word) != -1:
            scientific_result = 1
        if x['TI'] is not np.nan and x['TI'].lower().find(word) != -1:
            intervention_result = 1
    if intervention_result == 1 or public_result == 1 or scientific_result == 1:
        result_list.append("瑜伽")

    public_result, scientific_result, intervention_result = get_result_zero()
    for word in theme_word_dict['疫苗(vaccine)']:
        if x['AB'] is not np.nan and x['AB'].lower().find(word) != -1:
            public_result = 1
        if x['DE'] is not np.nan and x['DE'].lower().find(word) != -1:
            scientific_result = 1
        if x['TI'] is not np.nan and x['TI'].lower().find(word) != -1:
            intervention_result = 1
    if intervention_result == 1 or public_result == 1 or scientific_result == 1:
        result_list.append("疫苗")

    public_result, scientific_result, intervention_result = get_result_zero()
    for word in theme_word_dict['药物(Chemicals and Drugs)']:
        if x['AB'] is not np.nan and x['AB'].lower().find(word) != -1:
            public_result = 1
            drug_name.append(word)
        if x['DE'] is not np.nan and x['DE'].lower().find(word) != -1:
            scientific_result = 1
            drug_name.append(word)
        if x['TI'] is not np.nan and x['TI'].lower().find(word) != -1:
            intervention_result = 1
            drug_name.append(word)
    if intervention_result == 1 or public_result == 1 or scientific_result == 1:
        drug_name = list(set(drug_name))
        result = []
        for i in range(len(drug_name)):
            is_repeat = False
            for j in range(len(drug_name)):
                if i != j and drug_name[j].find(drug_name[i]) != -1:
                    is_repeat = True
            if not is_repeat:
                result.append(drugs_dict[drug_name[i]])
        drug_name = result
        result_list.append('药物')

    public_result, scientific_result, intervention_result = get_result_zero()
    for word in theme_word_dict['其他手段（others）']:
        if x['AB'] is not np.nan and x['AB'].lower().find(word) != -1:
            public_result = 1
        if x['DE'] is not np.nan and x['DE'].lower().find(word) != -1:
            scientific_result = 1
        if x['TI'] is not np.nan and x['TI'].lower().find(word) != -1:
            intervention_result = 1
    if intervention_result == 1 or public_result == 1 or scientific_result == 1:
        result_list.append('其他手段')

    # 最后整合一下
    if len(result_list) == 0:
        return "需要人工判断"
    return ','.join(result_list) + '|' + str(drug_name)


def get_type(data_path, temp_data_path, filter_data_path, dict_file_name):
    """
    Data and keywords match to get excel of clinical paper
     ID: What is the match?
     TI: One level lower than ID
     AB: lowest
     So first look at AB, look at TI, (vaccine), and then look at ID (including vaccine)
    :param data_path: excel file path, file after deduplication    path + "data_set/paper_1012_drop_duplicates.xlsx"
    :param temp_data_path Intermediate result path, keep the classification result of data_path (including mismatch)
      path + "data_set/paper_1012_drop_duplicates_filter_result.xlsx"
    :param filter_data_path Filtered path   path + "data_set/paper_1012_filter.xlsx"
    :param dict_file_name The path of intervention dictionary  path + "data_set/200924-临床关键词(论文、试验通用）.xlsx"
    :return:
    """
    # Get dictionary
    theme_word_dict, drugs_dict = get_dict(dict_file_name)
    # retrieve data
    data = pd.read_excel(data_path)
    print('The classification of intervention methods begins, and the data volume is' + str(len(data)))
    # 处理
    data['topic'] = data.apply(lambda x: get_type2(x, theme_word_dict, drugs_dict), axis=1)
    data['drugs'] = data['topic'].apply(lambda x: str(x.split('|')[1:]))
    data['topic'] = data['topic'].apply(lambda x: x.split('|')[0])
    data.to_excel(temp_data_path, index=None)
    data = data[data['topic'] != '需要人工判断']
    print('The classification of intervention methods ends, and the amount of data is' + str(len(data)))
    data.to_excel(filter_data_path, index=None)


def get_ut_list(excel_file_name):
    data = pd.read_excel(excel_file_name)
    data = list(data['UT'])
    data = list(set(data))
    data_str = ''
    for data_one in data:
        data_str = data_str + ' OR UT=' + str(data_one)

    print(data_str)
    print('The total length is' + str(len(data)))


def load_data(wos_file_name, country_dict_name, org_dict_name, financial_dict_name):
    # Get raw data
    data = pd.read_excel(wos_file_name, index=None)
    # Get national dictionary
    country_data = pd.read_excel(country_dict_name)
    country_dict = {}
    eu_list = []
    for index, row in country_data.iterrows():
        if not pd.isnull(row['result']):
            country_dict[row['country']] = row['result']
        if not pd.isnull(row['is_Europe']) and row['is_Europe'] == 'Europe':
            eu_list.append(row['result'])
    # Get institution dictionary
    org_df = pd.read_excel(org_dict_name)
    org_dict = {}
    for index, row in org_df.iteritems():
        org_dict[index.lower()] = index
        row = list(set(row))
        for row_one in row:
            if row_one is not None and row_one is not np.nan:
                org_dict[row_one.lower()] = index
    # Funding Agency Dictionary
    financial_df = pd.read_excel(financial_dict_name)
    financial_dict = {}
    for index, row in financial_df.iterrows():
        financial_dict[row['资助机构']] = row['同义词']

    return data, country_dict, org_dict, eu_list, financial_dict


def get_excel_table(path, wos_file_name, country_dict_name, org_dict_name, financial_dict_name):
    """
    Thesis, author, institution-country-change country belongs to the EU, institution-country, discipline table
    :param path: path路径
    :param wos_file_name: paper路径
    :param country_dict_name: 国家同义词表
    :param org_dict_name: 机构同义词表
    :param financial_dict_name: 资助机构同义词表
    :return:
    """
    # Root directory for saving data
    save_root = path + 'data_set/paper_csv/'
    data, country_dict, org_dict, eu_list, financial_dict = load_data(wos_file_name, country_dict_name, org_dict_name,
                                                                      financial_dict_name)
    paper_need_col = ["SO", "PT", "PY", "WC", "LA",  "PD", "EA", "Z9", "TC", 'month',
                      'UT',  "topic", 'label']

    paper = pd.DataFrame()  # Table 1: Paper table
    paper_country_org = pd.DataFrame()  # Table 2: Country-Institution-Institution Type-Team Table-European or not, the organization type will be added later
    paper_financial = pd.DataFrame()  # Table 3: Thesis-funding agency table
    paper_author = pd.DataFrame()  # Table 4: Paper-Author Table
    paper_wc = pd.DataFrame()  # Table 5: Paper-WC table

    print("Start processing：", datetime.datetime.now().strftime('%Y.%m.%d-%H:%M:%S'))
    for index, row in data.iterrows():
        # Table 1: One row corresponds to the generation of a record
        one_paper = {"id": index}
        for item in paper_need_col:
            if item in row and not pd.isnull(row[item]):
                one_paper[item] = row[item]
            else:
                one_paper[item] = None
        paper = paper.append([one_paper], ignore_index=True)

        # Table 2: C1 field splits countries and institutions
        if "C1" in row and not pd.isnull(row["C1"]):
            address_list = row["C1"].split("\n   ")
            if "AF" in row and not pd.isnull(row["AF"]):
                author_list = row['AF'].split("\n   ")
            for one_address in address_list:
                country = one_address.split(",")[-1].strip().lower()  # Split country field
                if one_address.find("[") >= 0 and one_address.find("]") >= 0:
                    org = one_address.split("]")[1].strip().split(",")[0].lower()
                    if org in ['usa', 'us army', 'usda', 'us epa', 'univ texas', 'usgs', 'nih', 'natl inst hlth',
                               'usn', 'us naval', 'us navy']:
                        org = one_address.split("]")[1].strip().split(",")[0].lower() + ', ' + \
                              one_address.split("]")[1].strip().split(",")[1].lower()
                    team = one_address.split("]")[0].strip()
                    team = team[team.find("[") + 1:]
                    # Delete the author who has appeared
                    team = team.split(",")
                else:
                    org = one_address.strip().split(",")[0].lower()
                    if org in ['usa', 'us army', 'usda', 'us epa', 'univ texas', 'usgs', 'nih', 'natl inst hlth',
                               'usn', 'us naval', 'us navy']:
                        org = one_address.strip().split(",")[0].lower() + ', ' + \
                              one_address.strip().split(",")[1].lower()
                    team = ", ".join(author_list)
                # Country synonym processing
                country_clear = country[:-1]
                if country_dict.__contains__(country_clear):
                    country_clear = country_dict[country_clear]
                country_clear = 'USA' if country_clear.endswith(' usa') else country_clear
                is_eu = 1 if country_clear in eu_list else 0
                # Institutional Synonym Processing
                org_clear = org
                if org_dict.__contains__(org_clear):
                    org_clear = org_dict[org_clear]
                one_record = {"paper_id": index, "country": country[:-1].lower(), "country_clear": country_clear,
                              "org": org, "org_clear": org_clear, 'is_eu': is_eu, "org_type": None, "team": team}
                paper_country_org = paper_country_org.append([one_record], ignore_index=True)

        # FU split (FU; followed by -)
        if "FU" in row and not pd.isnull(row["FU"]):
            import re
            p1 = re.compile(r'[(](.*?)[)]', re.S)  # Minimum match
            row['FU'] = row['FU'].replace('\n   ', ' ').lower()
            financial_list = row['FU'].split(";")
            for one_financial in financial_list:
                if one_financial.find("[") != -1:
                    financial_code = one_financial[one_financial.find("[") + 1:one_financial.find("]")].strip()
                    financial_name = one_financial[:one_financial.find("[")].strip()
                else:
                    financial_code = one_financial.strip()
                    financial_name = one_financial.strip()
                financial_name_list = financial_name.split("-")
                for financial_name_one in financial_name_list:
                    financial_name_one_list = re.findall(p1, financial_name_one)
                    financial_name_one_list = list(set(financial_name_one_list))
                    if len(financial_name_one_list) > 1:
                        print(financial_name_one_list)
                        print('--------------')
                    elif len(financial_name_one_list) == 0:
                        financial_name_one_list = [financial_name_one]
                    for a in financial_name_one_list:
                        if financial_dict.__contains__(a):
                            a = financial_dict[a]
                        paper_financial = paper_financial.append([{"paper_id": index, "financial_name": a,
                                                                   "financial_code": financial_code, "type": None}],
                                                                 ignore_index=True)

        # Split WC field
        if "WC" in row and not pd.isnull(row["WC"]):
            author_list = row['WC'].replace('\n   ', ' ').split(";")
            for author in author_list:
                one_author = {"paper_id": index, "wc": author.strip()}
                paper_wc = paper_wc.append([one_author], ignore_index=True)

        # Split AF field
        if "AF" in row and not pd.isnull(row["AF"]):
            author_list = row['AF'].split("\n")
            for author in author_list:
                one_author = {"paper_id": index, "author": author.strip()}
                paper_author = paper_author.append([one_author], ignore_index=True)

        if index%100 == 0 and index!=0:
            print("已处理", index, "条数据", datetime.datetime.now().strftime('%Y.%m.%d-%H:%M:%S'))

    # Several record sheets to save
    data['paper_id'] = list(data.index)
    paper_country_org['id'] = list(paper_country_org.index)
    paper_financial['id'] = list(paper_financial.index)
    paper_author['id'] = list(paper_author.index)
    paper_wc['id'] = list(paper_wc.index)
    data.to_excel(save_root + "paper_need_col.xlsx", index=False)  # The most primitive, keep all fields
    paper.to_excel(save_root + "paper.xlsx", index=False)
    paper_country_org.to_excel(save_root + "paper_country.xlsx", index=False)
    paper_financial.to_excel(save_root + "paper_financial.xlsx", index=False)
    paper_author.to_excel(save_root + "paper_author.xlsx", index=False)
    paper_wc.to_excel(save_root + "paper_wc.xlsx", index=False)

    print("The paper table split is completed！")


