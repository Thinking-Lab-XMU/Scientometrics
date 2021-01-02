
import datetime
import re

import pandas as pd
import numpy as np


def is_cancel(x):
    if str(x).lower().startswith('cancelled by'):
        return True
    if str(x).lower().startswith('cancelled due to'):
        return True
    if str(x).lower().startswith('retracted due to'):
        return True
    return False


def trial_excel(trail_file_name, cancel_file_name, drop_file_name, duplicates_file):
    """
    # Perform data filtering, including de-duplication, de-cancellation, and non-intrusive
    :param trail_file_name: Downloaded excel file
    :param cancel_file_name: Canceled trial data file
    :param drop_file_name:  File after data filtering
    :return:
    """
    data = pd.read_excel(trail_file_name)
    # First judge whether there are duplicates (ID, according to two titles)
    print('The total amount of clinical trial data is：' + str(len(data)))
    data.drop_duplicates(subset=['TrialID'], inplace=True)
    print('After the clinical trial TrialID is deduplicated, the total amount of data is：' + str(len(data)))
    data = data[~ data['TrialID'].isin(['ChiCTR2000031023', 'NCT04344106', 'NCT04319445'])]
    print('Remove several pieces of data that were manually excluded before, and the total amount of data is：' + str(len(data)))
    # Remove canceled trials
    data['is_cancel'] = data['Public title'].apply(lambda x: is_cancel(x))
    data_cancel = data[data['is_cancel'] == True]
    data_cancel.to_excel(cancel_file_name, index=False)
    data = data[data['is_cancel'] == False]
    print('After removing the cancellation trial, the total amount of data is:：' + str(len(data)))
    # Remove non-invasive tests
    intervention_list = ['Interventional clinical trial of medicinal product', 'Interventional', 'Interventional study', 'Intervention']
    data = data[data['Study type'].isin(intervention_list)]
    print('After removing non-invasive trials, the total amount of data is：' + str(len(data)))
    data['介入手段'] = data['Intervention']
    data['国家'] = data['Countries']
    # Remove data whose year is not 2020
    data['is_year'] = data['Date registration3'].apply(lambda x: str(x)[0:4])
    data = data[data['is_year'] == '2020']
    print('Excluding the data of other years, the total amount of data is：' + str(len(data)))
    # Remove duplicate data in two titles
    data_drop = data[data.duplicated(subset=['Public title', 'Scientific title', '介入手段'], keep=False)]
    data_drop.to_excel(duplicates_file)
    data.drop_duplicates(subset=['Public title', 'Scientific title', '介入手段'], inplace=True)
    print('After removing the duplicates of the two titles of the clinical trial, the total amount of data is：' + str(len(data)))
    data.to_excel(drop_file_name, index=False)


# -------------------Intervention method screening----------------------
def get_dict(dict_file_name):
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


def get_type1(x, theme_word_dict):
    # 获取治疗/预防类型
    zhiliao_result = ''
    public_result, scientific_result, intervention_result = get_result_zero()
    for word in theme_word_dict['治疗']:
        if x['Public title'].lower().find(word) != -1:
            public_result = 1
        if x['Scientific title'].lower().find(word) != -1:
            scientific_result = 1
        if x['介入手段'] is not np.nan and x['介入手段'].lower().find(word) != -1:
            intervention_result = 1
    if public_result + scientific_result + intervention_result >= 1:
        zhiliao_result = "治疗"

    yufang_result = ''
    public_result, scientific_result, intervention_result = get_result_zero()
    for word in theme_word_dict['预防']:
        if x['Public title'].lower().find(word) != -1:
            public_result = 1
        if x['Scientific title'].lower().find(word) != -1:
            scientific_result = 1
        if x['介入手段'] is not np.nan and x['介入手段'].lower().find(word) != -1:
            intervention_result = 1
    if public_result + scientific_result + intervention_result >= 1:
        yufang_result = "预防"

    if zhiliao_result == '' and yufang_result == '':
        return "介入方式不明"
    if zhiliao_result == '' or yufang_result == '':
        return zhiliao_result + yufang_result
    return zhiliao_result + "/" + yufang_result


def get_type2_method1(x, theme_word_dict, drugs_dict):
    # if x['type1'] == "需要人工判断":
    #     return "需要人工判断"
    # 中医药 药物 疫苗 非药物
    drug_name = []
    result_list = []

    public_result, scientific_result, intervention_result = get_result_zero()
    for word in theme_word_dict['中医药(Traditional Chinese Medicine)']:
        if x['Public title'].lower().find(word) != -1:
            public_result = 1
        if x['Scientific title'].lower().find(word) != -1:
            scientific_result = 1
        if x['介入手段'] is not np.nan and x['介入手段'].lower().find(word) != -1:
            intervention_result = 1
    if intervention_result == 1 or public_result + scientific_result == 2:
        result_list.append("中医药")

    public_result, scientific_result, intervention_result = get_result_zero()
    for word in theme_word_dict['AYUSH(Ayurveda, Yoga & Naturopathy, Unani, Siddha and Homoeopathy)']:
        if x['Public title'].lower().find(word) != -1:
            public_result = 1
        if x['Scientific title'].lower().find(word) != -1:
            scientific_result = 1
        if x['介入手段'] is not np.nan and x['介入手段'].lower().find(word) != -1:
            intervention_result = 1
    if intervention_result == 1 or public_result + scientific_result == 2:
        result_list.append("瑜伽")

    public_result, scientific_result, intervention_result = get_result_zero()
    for word in theme_word_dict['疫苗(vaccine)']:
        if x['Public title'].lower().find(word) != -1:
            public_result = 1
        if x['Scientific title'].lower().find(word) != -1:
            scientific_result = 1
        if x['介入手段'] is not np.nan and x['介入手段'].lower().find(word) != -1:
            intervention_result = 1
    if intervention_result == 1 or public_result + scientific_result == 2:
        result_list.append("疫苗")

    public_result, scientific_result, intervention_result = get_result_zero()
    for word in theme_word_dict['药物(Chemicals and Drugs)']:
        if x['Public title'].lower().find(word) != -1:
            public_result = 1
            drug_name.append(word)
        if x['Scientific title'].lower().find(word) != -1:
            scientific_result = 1
            drug_name.append(word)
        if x['介入手段'] is not np.nan and x['介入手段'].lower().find(word) != -1:
            intervention_result = 1
            drug_name.append(word)
    if intervention_result == 1 or public_result + scientific_result == 2:
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
        if x['Public title'].lower().find(word) != -1:
            public_result = 1
        if x['Scientific title'].lower().find(word) != -1:
            scientific_result = 1
        if x['介入手段'] is not np.nan and x['介入手段'].lower().find(word) != -1:
            intervention_result = 1
    if intervention_result == 1 or public_result + scientific_result == 2:
        result_list.append('其他手段')

    # 最后整合一下
    if len(result_list) == 0:
        return "需要人工判断"
    return ','.join(result_list) + '|' + str(drug_name)


def modify_type(x):
    if x['type1'] == '介入方式不明':
        if x['type2'] == '疫苗':
            return "预防"
        else:
            return "治疗"
    return x['type1']


def get_type(dict_file_name, input_file_name, temp_file_name, filter_data_path):
    """
    Data and keywords match, get excel for clinical trials, besides intervention, there are also treatment/prevention classification       :param input_file_name: excel文件路径, 去重后的文件
       :param temp_file_name Intermediate result path, keep the classification result of data_path (including mismatch)
       :param filter_data_path Filtered path
       :param dict_file_name The path of intervention dictionary  path + "data_set/200924-临床关键词(论文、试验通用）.xlsx"
       :return:
    """
    # Get keyword dictionary
    theme_word_dict, drugs_dict = get_dict(dict_file_name)
    # Get data and process it
    test_data = pd.read_excel(input_file_name)
    test_data = test_data.fillna('')
    test_data['type1'] = test_data.apply(lambda x: get_type1(x, theme_word_dict), axis=1)
    test_data['type2'] = test_data.apply(lambda x: get_type2_method1(x, theme_word_dict, drugs_dict), axis=1)
    test_data.to_excel(temp_file_name, index=False)
    # Remove data that requires manual judgment
    test_data = test_data[test_data['type2'] != '需要人工判断']
    print('After removing the data that requires manual judgment, the amount of data is：' + str(len(test_data)))
    test_data['type1'] = test_data.apply(lambda x: modify_type(x), axis=1)
    test_data['topic'] = test_data['type2'].apply(lambda x: x.split('|')[0])
    test_data['drugs'] = test_data['type2'].apply(lambda x: str(x.split('|')[1:]))

    test_data.to_excel(filter_data_path, index=False)


# -------------------Blind judgment----------------------
def suiji(row, suiji_dict):
    if suiji_dict.__contains__(str(row.lower())):
        return suiji_dict[str(row.lower())]

    if row.startswith('Randomized, Parallel'):
        return 1
    # 格式 Allocation: XX.
    target_list = re.findall(re.compile(r'Allocation: (.*?)[\.;]', re.S), str(row))
    if len(target_list) == 1:
        if target_list[0] in ['Non-Randomized', 'Non-randomised trial', 'Non-randomized controlled trial']:
            return 0
        elif target_list[0] in ['Randomized', 'Randomised controlled trial', 'Randomized controlled trial', 'Randomized trial']:
            return 1
        elif target_list[0] in ['N/A', 'N/A: single arm study']:
            return 0
        else:
            return None
    # format Randomization: XX,
    target_list = re.findall(r"Randomization: (.*?)[,.]", str(row))
    if len(target_list) == 1:
        if target_list[0] in ['Not randomized']:
            return 0
        elif target_list[0] in ['Randomized', 'Randomized trial', 'Randomized controlled trial']:
            return 1
        elif target_list[0] in ['N/A']:
            return 0
        else:
            return None
    # format Randomised: XXX<br>
    target_list = re.findall(r"Randomi[sz]ed: (.*?)[<,\n]", str(row))
    if len(target_list) == 1:
        # m.extend(target_list)
        if target_list[0] in ['no', 'No']:
            return 0
        elif target_list[0] in ['yes', 'Yes']:
            return 1
        elif target_list[0] in ['']:
            return 'N/A'
        else:
            return None
    # 格式: Primary purpose:
    target_list = re.findall(r"Primary purpose: (.*?)[.]", str(row))
    if len(target_list) == 1:
        if target_list[0] in ['Basic Science', 'Supportive Care', 'Other']:
            return '怀疑不是临床试验'
        else:
            return 0
    # 格式: Method of generating randomization sequence:
    if str(row).find('Method of generating randomization sequence:Computer generated randomization') != -1:
        return 1
    if str(row).find('Method of generating randomization sequence:Not Applicable') != -1:
        return 0
    if row.startswith('Non-randomized') or 'non-randomized' in row:
        return 0
    # # 逗号分开
    target_list = row.lower().split(',')
    target_list = [i.strip() for i in target_list]
    if 'randomized' in target_list or 'randomised' in target_list or 'randomized-controlled' in target_list or 'randomised-controlled' in target_list or 'randomized controlled trial' in target_list\
            or 'd8110c00001 is a phase III randomized' in target_list:
        return 1
    return None


def duizhao(row, duizhao_dict):
    if duizhao_dict.__contains__(str(row.lower())):
        return duizhao_dict[str(row.lower())]

    # format Intervention model: XX.
    target_list = re.findall(re.compile(r'Intervention model: (.*?)[\.;]', re.S), str(row))
    if len(target_list) == 1:
        if target_list[0] in ['Parallel Assignment', 'Factorial Assignment', 'Crossover Assignment']:
            return 1
        elif target_list[0] in ['Single Group Assignment', 'Sequential Assignment']:
            return 0
        else:
            return None
    # format Assignment: XX,
    target_list = re.findall(r"Assignment: (.*?)[,.,;]", str(row))
    if len(target_list) == 1:
        if target_list[0] in ['Parallel', 'Factorial', 'Crossover']:
            return 1
        elif target_list[0] in ['Single (group)', 'Single group', 'Single']:
            return 0
        elif target_list[0] in ['Other']:
            return 'N/A'
        else:
            return None
    # format Control: XXX<br>
    target_list = re.findall(r"Control: (.*?)[<\n,]", str(row))
    if len(target_list) == 1:
        # m.extend(target_list)
        if target_list[0] in ['Not applicable']:
            return 0
        else:
            return 1
    # format Controlled: XXX<br>
    target_list = re.findall(r"Controlled: (.*?)[(<br>)\n,]", str(row))
    if len(target_list) == 1:
        if target_list[0] in [' randomized-controlled', 'yes']:
            return 1
        elif target_list[0] in ['no']:
            return 0
    # format Allocation: XX.
    target_list = re.findall(re.compile(r'Allocation: (.*?)[\.;]', re.S), str(row))
    if len(target_list) == 1:
        if target_list[0] in ['Randomised controlled trial']:
            return 1
        elif target_list[0] in ['Non-randomised trial']:
            return 'N/A'
        else:
            return None
    # others
    if row.startswith('Randomized, Parallel Group'):
        return 1
    if row.startswith('Factorial: participants randomly allocated to either no, one, some or all interventions simultaneously,Randomised,Simple randomization using'):
        return 'N/A'
    if row.startswith('Non-Randomized, Parallel Group, Placebo Controlled Trial') or row.startswith(
            'Non-Randomized, Parallel Group, Active Controlled Trial') or row.startswith(
            'Non-randomized, Active Controlled Trial'):
        return 1
    target_list = row.lower().split(',')
    target_list = [i.strip() for i in target_list]
    if 'placebo-controlled' in target_list or 'controlled' in target_list or 'randomised- controlled' in target_list or 'randomized-controlled' in target_list:
        return 1
    if 'randomised controlled' in target_list or 'randomized controlled trial' in target_list or 'placebo-controlled' in target_list:
        return 1
    if 'non-randomized controlled trial' in target_list:
        return 0
    return None


def mangfa(row, mangfa_dict):
    if mangfa_dict.__contains__(str(row.lower())):
        return mangfa_dict[str(row.lower())]
    # format Masking: XX.
    target_list = re.findall(re.compile(r'Masking: (.*?)[\.;,(]', re.S), str(row))
    if len(target_list) == 1:
        if target_list[0].strip() in ['Single']:
            return 1
        elif target_list[0].strip() in ['None', 'Open']:
            return 0
        elif target_list[0].strip() in ['Double', 'Double Blind', 'Blinded']:
            return 2
        elif target_list[0].strip() in ['Triple']:
            return 3
        elif target_list[0].strip() in ['Quadruple']:
            return 4
        else:
            return None
    # format Blinding: XX,
    target_list = re.findall(r"Blinding: (.*?)[,.,;]", str(row))
    # m.extend(target_list)
    if len(target_list) == 1:
        if target_list[0].strip() in ['Single blinded']:
            return 1
        elif target_list[0].strip() in ['Not blinded', 'Open']:
            return 0
        elif target_list[0].strip() in ['Double blinded']:
            return 2
        elif target_list[0].strip() in ['Triple blinded']:
            return 3
        elif target_list[0].strip() in ['Quadruple']:
            return 0
        else:
            return None
    # format Double blind: XXX<br>
    zero = 0
    target_list = re.findall(r"Double blind: (.*?)[<\n]", str(row))
    # m.extend(target_list)
    if len(target_list) == 1:
        if target_list[0] in ['yes']:
            return 2
        else:
            zero = zero - 1
    # format Single blind: XXX<br>
    target_list = re.findall(r"Single blind: (.*?)[<\n]", str(row))
    # m.extend(target_list)
    if len(target_list) == 1:
        if target_list[0] in ['yes']:
            return 1
        else:
            zero = zero - 1
    # format Open: XXX<br>
    target_list = re.findall(r"Open: (.*?)[<\n]", str(row))
    # m.extend(target_list)
    if len(target_list) == 1:
        if target_list[0] in ['yes']:
            return 0
    if zero == -2:
        return 0
    # format Blinding and masking: XXX
    target_list = re.findall(r"Blinding and masking:(.*)", str(row))
    if len(target_list) == 1:
        if target_list[0] in ['Outcome Assessor Blinded']:
            return 1
        elif target_list[0] in ['Open Label', ]:
            return 0
        elif target_list[0] in ['Double Blind Double Dummy',
                                'Participant, Investigator, Outcome Assessor and Date-entry Operator Blinded',
                                'Participant and Outcome Assessor Blinded',
                                'Participant and Investigator Blinded',
                                'Participant Blinded']:
            return 2
        elif target_list[0] in ['Not Applicable']:
            return 'N/A'
        elif target_list[0] in ['Participant, Investigator and Outcome Assessor Blinded']:
            return 3
        else:
            return None
    # Comma separated
    target_list = row.lower().split(',')
    target_list = [i.strip() for i in target_list]  #
    if '3-arm open' in target_list or 'open' in target_list or 'open label' in target_list or 'open(masking not used)' in target_list or 'open clinical trial with two arms.' in target_list:
        return 0
    if 'Single-blind randomised efficacy' in target_list or 'single-masked' in target_list \
            or 'single blind' in target_list or 'single-blind' in target_list:
        return 1
    if 'double blind' in target_list or 'double-blind' in target_list or 'double-blind.' in target_list \
            or 'double blinded' in target_list or 'double-blinded' in target_list:
        return 2
    return None


def get_blind_result(data_file, suiji_dict, to_suiji_file, duizhao_dict, to_duizhao_file, mangfa_dict, to_mangfa_file, result_file):
    """
    Obtain the results of blinding and other methods
    :param data_file: trial data file
    :param suiji_dict: Random dictionary
    :param to_suiji_file: No data matching the classification
    :param duizhao_dict:
    :param to_duizhao_file:
    :param mangfa_dict:
    :param to_mangfa_file:
    :param result_file: Add three columns of test data files
    :return:
    """
    data = pd.read_excel(data_file)
    # TODO: Read the file, perform the corresponding first
    suiji_data = pd.read_excel(suiji_dict)
    suiji_data = suiji_data.dropna()
    suiji_data['随机'] = suiji_data['随机'].apply(lambda x: x if x != 'N' else 'N/A')
    suiji_dict = {}
    for index, row in suiji_data.iterrows():
        suiji_dict[row['表述方式'].lower()] = row['随机']
    data['随机'] = data['Study design'].apply(lambda x: suiji(x, suiji_dict))
    data.loc[data['TrialID'] == 'NCT04325672', '随机'] = 'N/A'
    data.loc[data['TrialID'] == 'ChiCTR2000032716', '随机'] = 'N/A'
    data_result = data[(data['随机'].isna())]
    data_result = data_result[['Study design']]
    data_result.to_excel(to_suiji_file)

    duizhao_data = pd.read_excel(duizhao_dict)
    duizhao_data = duizhao_data.dropna()
    duizhao_data['对照'] = duizhao_data['对照'].apply(lambda x: x if x != 'N' else 'N/A')
    duizhao_dict = {}
    for index, row in duizhao_data.iterrows():
        duizhao_dict[row['表述方式'].lower()] = row['对照']
    data['对照'] = data['Study design'].apply(lambda x: duizhao(x, duizhao_dict))
    data.loc[data['TrialID'] == 'NCT04325672', '对照'] = '0'
    data.loc[data['TrialID'] == 'ChiCTR2000032716', '对照'] = 'N/A'
    data_result = data[data['对照'].isna()]
    data_result = data_result[['Study design']]
    data_result.to_excel(to_duizhao_file)

    mangfa_data = pd.read_excel(mangfa_dict)
    mangfa_data = mangfa_data.dropna()
    mangfa_data['盲法'] = mangfa_data['盲法'].apply(lambda x: x if x != 'N' else 'N/A')
    mangfa_dict = {}
    for index, row in mangfa_data.iterrows():
        mangfa_dict[row['表述方式'].lower()] = row['盲法']
    data['盲法'] = data['Study design'].apply(lambda x: mangfa(x, mangfa_dict))
    data.loc[data['TrialID'] == 'NCT04325672', '盲法'] = '0'
    data.loc[data['TrialID'] == 'ChiCTR2000032716', '盲法'] = 'N/A'
    data_result = data[data['盲法'].isna()]
    data_result = data_result[['Study design']]
    data_result.to_excel(to_mangfa_file)

    data.to_excel(result_file, index=False)
    print('Blind judgment is over, look at the data manually！')


# --------------------------Get form-----------------
def load_data(trail_file_name, country_dict_name):
    # Get raw data
    data = pd.read_excel(trail_file_name, index=None)
    # Get national dictionary
    country_data = pd.read_excel(country_dict_name)
    country_dict = {}
    eu_list = []
    for index, row in country_data.iterrows():
        if not pd.isnull(row['result']):
            country_dict[row['country']] = row['result']
        if not pd.isnull(row['is_Europe']) and row['is_Europe'] == 'Europe':
            eu_list.append(row['result'])

    return data, country_dict, eu_list


def get_trail_table(path, trail_file_name, country_dict_name):
    """
    Split country and author
    :param path:
    :param trail_file_name:
    :param country_dict_name:
    :return:
    """
    # Root directory for saving data
    save_root = path + 'data_set/paper_csv/'
    data, country_dict, eu_list = load_data(trail_file_name, country_dict_name)

    data['month'] = data['Date registration3'].apply(lambda x: str(x)[4:6])
    paper_need_col = ["TrialID", "Countries", 'Source Register', 'month', "topic", 'label']

    trail = pd.DataFrame()  # 表1：试验表
    trial_country = pd.DataFrame()  # 表2：试验-国家
    trail_author = pd.DataFrame()  # 表5：试验-作者表

    print("Start processing：", datetime.datetime.now().strftime('%Y.%m.%d-%H:%M:%S'))
    for index, row in data.iterrows():
        # Table 1: Generation of one row corresponding to one record
        one_paper = {"id": index}
        for item in paper_need_col:
            if item in row and not pd.isnull(row[item]):
                one_paper[item] = row[item]
            else:
                one_paper[item] = None
        trail = trail.append([one_paper], ignore_index=True)

        # Table 2: Country field split country
        if not pd.isnull(row["国家"]):
            country_list = row["国家"].lower().strip().split(";")
            for country_clear in country_list:
                if country_dict.__contains__(country_clear):
                    country_clear = country_dict[country_clear]
                is_eu = 1 if country_clear in eu_list else 0
                if country_clear != 'Europe':
                    one_record = {"paper_id": index, "country": country_clear, 'is_eu': is_eu}
                else:
                    one_record = {"paper_id": index, "country": None, 'is_eu': is_eu}
                trial_country = trial_country.append([one_record], ignore_index=True)

        # 表5：拆分作者
        author_list = []
        if not pd.isnull(row["Contact Firstname"]) and pd.isnull(row["Contact Lastname"]):
            if row["Contact Firstname"].find(';') != -1:
                author_list.extend(row["Contact Firstname"].split(';'))
            elif row["Contact Firstname"].find(',') != -1:
                author_list.extend(row["Contact Firstname"].split(','))
            else:
                author_list.extend(row["Contact Firstname"].split('-'))

        if not pd.isnull(row["Contact Lastname"]) and pd.isnull(row["Contact Firstname"]):
            if row["Contact Lastname"].find(';') != -1:
                author_list.extend(row["Contact Lastname"].split(';'))
            elif row["Contact Lastname"].find(',') != -1:
                author_list.extend(row["Contact Lastname"].split(','))
            else:
                author_list.extend(row["Contact Lastname"].split('-'))

        if not pd.isnull(row["Contact Lastname"]) and not pd.isnull(row["Contact Firstname"]):
            first_list = row["Contact Lastname"].split(';')
            last_list = row["Contact Lastname"].split(';')
            if len(first_list) != len(last_list):
                print(row['TrialID'])
            for i in range(0, len(first_list)):
                author_list.append(first_list[i] + ' ' + last_list[i])

            for author in author_list:
                one_author = {"paper_id": index, "author": author.strip()}
                trail_author = trail_author.append([one_author], ignore_index=True)

        if index % 100 == 0 and index != 0:
            print("Processed", index, "data", datetime.datetime.now().strftime('%Y.%m.%d-%H:%M:%S'))

    # Several record sheets to save
    data['paper_id'] = list(data.index)
    trial_country['id'] = list(trial_country.index)
    trail_author['id'] = list(trail_author.index)
    data.to_excel(save_root + "trail_need_col.xlsx", index=False)
    trail.to_excel(save_root + "trail.xlsx", index=False)
    trial_country.to_excel(save_root + "trial_country.xlsx", index=False)
    trail_author.to_excel(save_root + "trail_author.xlsx", index=False)

    print("试验表拆分完成！")