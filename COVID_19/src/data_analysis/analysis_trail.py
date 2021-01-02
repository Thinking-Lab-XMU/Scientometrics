import re

import pandas as pd
import pymysql
import numpy as np


def get_connection():
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='covid', charset='utf8')
    cursor = conn.cursor()
    return conn, cursor


def close_connection(conn, cursor):
    cursor.close()
    conn.close()


# ----------------------------------注册平台部分----------------------------------
def get_source_number(paper_number_excel):
    """
    获取试验 的注册平台
    :param paper_number_excel:
    :return:
    """
    conn, cursor = get_connection()
    # 论文数目
    sql_paper = '''
        select  source_register, count(*) from trail
        group by source_register
        order by count(*) desc
    '''
    cursor.execute(sql_paper)
    result_paper = cursor.fetchall()
    result_paper = pd.DataFrame(result_paper, columns=['source_register', 'number'])
    # 存储
    result_paper.to_excel(paper_number_excel, index=None)
    close_connection(conn, cursor)


def source_some_country_number(wc, country_list, cursor):
    """
    某个国家某个来源的数目
    :param wc:
    :param country_list:
    :param cursor:
    :return:
    """
    sql = """
            select count(distinct id)
            from trail 
            where source_register = '%s'
            and id in  (SELECT paper_id  FROM trial_country where `country` = '%s')  
        """
    eu_sql = """
            select count(distinct id)
            from trail 
            where source_register = '%s'
            and id in  (SELECT paper_id  FROM trial_country where is_eu = 1)  
    """
    non_eu_sql = """
                select count(distinct id)
                from trail 
                where source_register = '%s'
                and id in  (SELECT paper_id  FROM trial_country where is_eu = 0)  
        """
    results = []
    for country in country_list:
        country_sql = sql % (wc, country)
        if country_sql == 'europe':
            country_sql = eu_sql % wc
        elif country_sql == 'non-europe':
            country_sql = non_eu_sql % wc
        cursor.execute(country_sql)
        result = cursor.fetchone()[0]
        results.append(result)
    return results


def source_top10_country(paper_number_excel, country_number_excel, paper_result_excel):
    """
    # 学科 某些国家的发文量
    # 国家列表
    # 查询paper 并 返回 月份， 按照月份统计
    :param country_number_excel: 从这个文件里获取国家
    :param paper_number_excel: 获取期刊
    :param paper_result_excel:
    :return:
    """
    conn, cursor = get_connection()
    paper_top10_list = list(pd.read_excel(paper_number_excel).head(10)['source_register'])
    data = pd.read_excel(country_number_excel)
    data = data[~ (data['country'] == 'europe')]
    data = data[~ (data['country'] == 'non-europe')]
    country_list = list(data.head(10)['country'])

    # 列名称
    columns = ['注册平台'] + country_list
    # ---论文---
    paper_result = []
    for i in range(len(paper_top10_list)):
        result_country = source_some_country_number(paper_top10_list[i], country_list, cursor)
        paper_result.append([paper_top10_list[i]] + result_country)
    paper_result = pd.DataFrame(paper_result, columns=columns)
    paper_result.to_excel(paper_result_excel, index=None)

    close_connection(conn, cursor)


def source_radio(data_excel, result_excel):
    """
    求百分比，每列数值除以每列的和
    :param data_excel:
    :param result_excel:
    :return:
    """
    data = pd.read_excel(data_excel, index_col=0)
    for column_name in list(data.columns):
        sum_count = data[column_name].sum()
        data[column_name] = data[column_name] / sum_count
    data.to_excel(result_excel)


# # ----------------------------------表格部分----------------------------------
def load_data(trail_file_name, country_dict_name):
    # 获取原始数据
    data = pd.read_excel(trail_file_name, index=None)
    # 获取国家字典
    country_data = pd.read_excel(country_dict_name)
    country_dict = {}
    eu_list = []
    for index, row in country_data.iterrows():
        if not pd.isnull(row['result']):
            country_dict[row['country']] = row['result']
        if not pd.isnull(row['is_Europe']) and row['is_Europe'] == 'Europe':
            eu_list.append(row['result'])

    return data, country_dict, eu_list


def get_blind_table(trail_file_name, country_dict_name, country_number_excel, phase_dict_file, phase_result_file,
                    size_dict_file, size_result_file, gender_dict_file, gender_result_file, age_dict_file,
                    data_result_file, result_file_with_number, result_file):
    """
    获得试验最终的统计表格
    :param trail_file_name: 试验数据文件
    :param country_dict_name: 国家字典
    :param country_number_excel: 从中获取要统计的国家列表，支持 Europe和 Global
    :param phase_dict_file: 阶段词典
    :param phase_result_file: 阶段的数据处理结果，去重后所有内容
    :param size_dict_file: 试验人数规模词典
    :param size_result_file: 试验人数规模结果(只有不匹配的)
    :param gender_dict_file: 性别字典
    :param gender_result_file: 性别的数据处理结果，去重后所有内容
    :param age_dict_file: 年龄字典，年龄需要每次人工更新
    :param data_result_file: 数据结果文件
    :param result_file_with_number: 结果文件，没有四分位值的那个
    :param result_file: 果文件，有四分位值的那个
    :return:
    """
    # 保存数据的根目录
    data, country_dict, eu_list = load_data(trail_file_name, country_dict_name)
    # 要统计的国家
    data_country = pd.read_excel(country_number_excel)
    # data_country = data_country[~ (data_country['country'] == 'europe')]
    region_list = ['Global'] + list(data_country.head(12)['country'])
    region_list[1] = 'non-eu'
    # 获得区域
    result = []
    for index, row in data.iterrows():
        if not pd.isnull(row["国家"]):
            country_list = row["国家"].lower().strip().split(";")
            country_clear_list = []
            for country_clear in country_list:
                if country_dict.__contains__(country_clear):
                    country_clear = country_dict[country_clear]
                is_eu = 1 if country_clear in eu_list else 0
                if is_eu == 0:
                    country_clear_list.extend([country_clear, 'non-eu'])
                else:
                    country_clear_list.extend([country_clear, 'europe'])
            country_clear_list.append('Global')
            country_clear_list = list(set(country_clear_list))
            result.append('|'.join(country_clear_list))
        else:
            result.append('')
    data['region'] = result
    # 进行统计
    # 对每个地区生成一列
    all_result = []
    for region in region_list:
        region_result = []
        # TODO:总数,治疗、预防、治疗/预防
        region_result.append(len(data[data["region"].str.contains(region)]))
        region_result.append(len(data[(data["region"].str.contains(region)) & (data["type1"] == "治疗")]))
        region_result.append(len(data[(data["region"].str.contains(region)) & (data["type1"] == "预防")]))
        region_result.append(len(data[(data["region"].str.contains(region)) & (data["type1"] == "治疗/预防")]))
        # TODO:介入手段 中医药，药物，疫苗，非药物
        region_result.append(len(data[(data["region"].str.contains(region)) & (data["topic"].str.contains("中医药"))]))
        region_result.append(len(data[(data["region"].str.contains(region)) & (data["topic"].str.contains("药物"))]))
        region_result.append(len(data[(data["region"].str.contains(region)) & (data["topic"].str.contains("疫苗"))]))
        region_result.append(len(data[(data["region"].str.contains(region)) & (data["topic"].str.contains("瑜伽"))]))
        region_result.append(len(data[(data["region"].str.contains(region)) & (data["topic"].str.contains("其他手段"))]))
        # TODO:临床试验阶段:0,1,2,3,4,N/A
        data["Phase"] = data["Phase"].fillna('N/A')
        data["Phase"] = data["Phase"].astype(str)
        data["Phase"].apply(lambda x: x.replace("\n", ';'))
        data["Phase"].apply(lambda x: x.replace("Human pharmacology (Phase I): yes", '1'))
        data["Phase"].apply(lambda x: x.replace("Therapeutic exploratory (Phase II): yes", '2'))
        data["Phase"].apply(lambda x: x.replace("Therapeutic confirmatory - (Phase III): yes", '3'))
        data["Phase"].apply(lambda x: x.replace("rapeutic use (Phase IV): yes", '4'))
        data["Phase"].apply(lambda x: x.replace("New Treatment Measure Clinical Study", '0'))

        phase_data = pd.read_excel(phase_dict_file)
        dict_phase = {}
        for index, row in phase_data.iterrows():
            dict_phase[row['Phase']] = row['result']
        data['Phase'] = data['Phase'].apply(lambda x: str(dict_phase[x]) if dict_phase.__contains__(x) else x)
        data['Phase'] = data['Phase'].apply(lambda x: np.nan if pd.isnull(x) else x)
        data["Phase"] = data["Phase"].fillna('N/A')
        phase_result = data['Phase'].drop_duplicates()
        phase_result.to_excel(phase_result_file)
        # 统计
        region_result.append(len(data[(data["region"].str.contains(region)) & (data["Phase"].str.contains('0'))]))
        region_result.append(len(data[(data["region"].str.contains(region)) & (data["Phase"].str.contains('1'))]))
        region_result.append(len(data[(data["region"].str.contains(region)) & (data["Phase"].str.contains('2'))]))
        region_result.append(len(data[(data["region"].str.contains(region)) & (data["Phase"].str.contains('3'))]))
        region_result.append(len(data[(data["region"].str.contains(region)) & (data["Phase"].str.contains('4'))]))
        region_result.append(len(data[(data["region"].str.contains(region)) & (data["Phase"].str.contains('5'))]))
        region_result.append(len(data[(data["region"].str.contains(region)) & (data["Phase"].str.contains('N/A'))]))
        # TODO: 招募状况：Recruiting,Not recruiting,Authorised,NA
        data["Recruitment Status"] = data["Recruitment Status"].fillna('N/A')
        data['Recruitment Status'] = data['Recruitment Status'].apply(lambda x: x if x != "Not Available" else "N/A")
        data['Recruitment Status'] = data['Recruitment Status'].apply(lambda x: x if x != "Not recruiting" else "Not Recruiting")
        region_result.append(
            len(data[(data["region"].str.contains(region)) & (data["Recruitment Status"] == "Recruiting")]))
        region_result.append(
            len(data[(data["region"].str.contains(region)) & (data["Recruitment Status"] == "Not Recruiting")]))
        region_result.append(
            len(data[(data["region"].str.contains(region)) & (data["Recruitment Status"] == "Authorised")]))
        region_result.append(len(data[(data["region"].str.contains(region)) & (data["Recruitment Status"] == "N/A")]))
        # TODO: 试验组规模:0,<50,50-99,100-499,500-999,1000-2499,2500-4999,5000-9999,>10000
        person_number = []
        person_no_number = []  # 匹配不到数值
        # 字典匹配
        size_data = pd.read_excel(size_dict_file)
        dict_size = {}
        for index, row in size_data.iterrows():
            dict_size[row['Target size']] = row['result']
        data['Target size'] = data['Target size'].apply(lambda x: dict_size[x] if dict_size.__contains__(x) else x)
        data["Target size"] = data["Target size"].fillna(-1)
        # 规则匹配
        for target_size in list(data['Target size']):
            target_list = re.findall(r":\d+", str(target_size))
            target_list = [i[1:] for i in target_list]
            if len(target_list) == 0:
                target_list = re.findall(r"^\d+[\.]*[\d+]*$", str(target_size))
            if len(target_list) == 0:
                person_no_number.append(str(target_size))
                person_number.append(-1)
            else:
                count = 0
                for i in target_list:
                    count = count + int(float(i))
                person_number.append(count)
        data['sum'] = person_number
        # 匹配不到结果输出
        person_no_number = pd.DataFrame(person_no_number, columns=['Target size'])
        person_no_number.to_excel(size_result_file)
        # 统计
        sum_mid = data[data["region"].str.contains(region)]['sum']
        region_result.append("%s (%s - %s)" % (sum_mid.median(), sum_mid.quantile(.25), sum_mid.quantile(.75)))

        region_result.append(len(data[(data["region"].str.contains(region)) & (data["sum"] >= 0) & (data["sum"] < 50)]))
        region_result.append(
            len(data[(data["region"].str.contains(region)) & (data["sum"] >= 50) & (data["sum"] <= 99)]))
        region_result.append(
            len(data[(data["region"].str.contains(region)) & (data["sum"] >= 100) & (data["sum"] <= 249)]))
        region_result.append(
            len(data[(data["region"].str.contains(region)) & (data["sum"] >= 250) & (data["sum"] <= 499)]))
        region_result.append(
            len(data[(data["region"].str.contains(region)) & (data["sum"] >= 500) & (data["sum"] <= 999)]))
        region_result.append(
            len(data[(data["region"].str.contains(region)) & (data["sum"] >= 1000) & (data["sum"] <= 4999)]))
        region_result.append(
            len(data[(data["region"].str.contains(region)) & (data["sum"] >= 5000) & (data["sum"] <= 9999)]))
        region_result.append(len(data[(data["region"].str.contains(region)) & (data["sum"] >= 10000)]))
        region_result.append(len(data[(data["region"].str.contains(region)) & (data["sum"] == -1)]))

        # TODO: Inclusion gender
        # 字典匹配
        gender_data = pd.read_excel(gender_dict_file)
        dict_gender = {}
        for index, row in gender_data.iterrows():
            dict_gender[row['Inclusion gender']] = row['result']
        data['Inclusion gender'] = data['Inclusion gender'].apply(lambda x: dict_gender[x] if dict_gender.__contains__(x) else x)
        data["Inclusion gender"] = data["Inclusion gender"].fillna('N/A')
        gender_result = data['Inclusion gender'].drop_duplicates()
        gender_result.to_excel(gender_result_file)
        # 统计
        region_result.append(len(data[(data["region"].str.contains(region)) & (data["Inclusion gender"] == 'Both')]))
        region_result.append(len(data[(data["region"].str.contains(region)) & (data["Inclusion gender"] == 'Male')]))
        region_result.append(len(data[(data["region"].str.contains(region)) & (data["Inclusion gender"] == 'Female')]))
        region_result.append(len(data[(data["region"].str.contains(region)) & (data["Inclusion gender"] == 'N/A')]))

        # TODO: Inclusion age (最小年龄，最大年龄，然后做区间判断)
        # 字典匹配
        age_data = pd.read_excel(age_dict_file)
        dict_age = {}
        for index, row in age_data.iterrows():
            dict_phase[row['Inclusion age']] = row['result']
        data['Inclusion agemin'] = data['Inclusion agemin'].apply(lambda x: dict_age[x] if dict_age.__contains__(x) else x)
        data['Inclusion agemax'] = data['Inclusion agemax'].apply(lambda x: dict_age[x] if dict_age.__contains__(x) else x)
        # 模式匹配
        data["Inclusion agemin"] = data["Inclusion agemin"].fillna('N/A')
        min_number = []
        for target_size in list(data['Inclusion agemin']):
            target_list = re.findall(r"\d+", str(target_size))  # 是月，除以12取整数。非整数，除以12取整数，其他的提取里面的整数(这里人工判断一下)
            count = 0
            for i in target_list:
                count = count + int(i)
            if count == 0:
                count = 'N/A'
            min_number.append(count)
        data['Inclusion agemin'] = min_number

        data["Inclusion agemax"] = data["Inclusion agemax"].fillna('N/A')
        max_number = []
        for target_size in list(data['Inclusion agemax']):
            target_list = re.findall(r"\d+", str(target_size))  # 是月，除以12取整数。非整数，除以12取整数，其他的提取里面的整数(这里人工判断一下)
            count = 0
            for i in target_list:
                count = count + int(i)
            if count == 0:
                count = 'N/A'
            max_number.append(count)
        data['Inclusion agemax'] = max_number
        # 各个时期
        min_list = [0, 15, 30, 45, 60, 70]
        max_list = [14, 29, 44, 59, 69, 200]
        for i in range(0, len(min_list)):
            result = []
            range_real = list(range(min_list[i], max_list[i]))
            range_len = len(range_real)
            for index, row in data.iterrows():
                min_age = row['Inclusion agemin']
                max_age = row['Inclusion agemax']
                if min_age == 'N/A' and max_age == 'N/A':
                    result.append(False)
                else:
                    if min_age == 'N/A':
                        min_age = 0
                    elif max_age == 'N/A':
                        max_age = 200
                    range_this = list(range(min_age, max_age))
                    range_in = set(range_real) & set(range_this)
                    if 2 * len(list(range_in)) >= range_len:
                        result.append(True)
                    else:
                        result.append(False)
            data[str(min_list[i])] = result
        # 统计
        region_result.append(len(data[(data["region"].str.contains(region)) & (data["0"] == True)]))
        region_result.append(len(data[(data["region"].str.contains(region)) & (data["15"] == True)]))
        region_result.append(len(data[(data["region"].str.contains(region)) & (data["30"] == True)]))
        region_result.append(len(data[(data["region"].str.contains(region)) & (data["45"] == True)]))
        region_result.append(len(data[(data["region"].str.contains(region)) & (data["60"] == True)]))
        region_result.append(len(data[(data["region"].str.contains(region)) & (data["70"] == True)]))
        region_result.append(len(data[(data["region"].str.contains(region)) & (data["Inclusion agemin"] == 'N/A') & (
                    data["Inclusion agemax"] == 'N/A')]))
        # TODO: 试验类型 ：随机加控制，不随机加控制，单臂。这个人工判断然后产生一列。 盲法，对照
        data['随机'] = data['随机'].fillna('N/A')
        data['随机'] = data['随机'].apply(lambda x: -1 if x == 'N/A' else int(x)).astype(int)
        data['对照'] = data['对照'].fillna('N/A')
        data['对照'] = data['对照'].apply(lambda x: -1 if x == 'N/A' else int(x)).astype(int)

        data['exper_type'] = -1
        data['exper_type'] = data.apply(lambda x:
                                        '随机加控制' if (int(x['对照']) == 1 and int(x['随机']) == 1) else (
                                            '不随机加控制' if (int(x['对照']) == 1 and int(x['随机']) == -1) else (
                                                '不随机加控制' if (int(x['对照']) == 1 and int(x['随机']) == 0) else (
                                                    '单臂' if int(x['对照']) == 0 else None))), axis=1)

        # [(data["对照"] == 1) & (data["随机"] == 1)]['exper_type'] = '随机加控制'
        # data[(data["对照"] == 1) & (data["随机"] == 0) ]['exper_type'] = '不随机加控制'
        # data[(data["对照"] == 1) & (data["随机"] == 'N/A') ]['exper_type'] = '不随机加控制'
        # data[data["对照"] == 0]['exper_type'] = '单臂'

        region_result.append(len(data[(data["region"].str.contains(region)) & (data["exper_type"] == '随机加控制')]))
        region_result.append(len(data[(data["region"].str.contains(region)) & (data["exper_type"] == '不随机加控制')]))
        region_result.append(len(data[(data["region"].str.contains(region)) & (data["exper_type"] == '单臂')]))
        # TODO:Blinded
        data["盲法"] = data["盲法"].apply(lambda x: x if x != 'N/A' else -1)
        data["盲法"] = data['盲法'].fillna(-1)
        region_result.append(len(data[(data["region"].str.contains(region)) & (data["盲法"] == 0)]))
        region_result.append(len(data[(data["region"].str.contains(region)) & (data["盲法"] == 1)]))
        region_result.append(len(data[(data["region"].str.contains(region)) & (data["盲法"] == 2)]))
        region_result.append(len(data[(data["region"].str.contains(region)) & (data["盲法"] >= 3)]))
        region_result.append(len(data[(data["region"].str.contains(region)) & (data["盲法"] == -1)]))
        # TODO：存储
        all_result.append(region_result)
    data.to_excel(data_result_file)
    # TODO: 存储
    all_result = pd.DataFrame(all_result)  # , columns=region_list
    all_result.index = region_list
    all_result = pd.DataFrame(all_result.T, index=all_result.columns, columns=all_result.index)
    all_result.to_excel(result_file)
    all_result.loc[20] = all_result.loc[20].apply(lambda x: int(float(x.split('(')[0].strip())))
    all_result.to_excel(result_file_with_number)


def get_blind_radio(data):
    result = []
    sum_data = data[0]
    result.append(sum_data)
    for i in range(1, 8 + 1):  # 到非医药
        m = data[i] / sum_data * 100
        if m == 0:
            result.append('0')
        else:
            result.append(str(data[i]) + str('(') + str("%.1f" % m) + '%)')
    for i in range(9, 14 + 1):  # 阶段
        m = data[i] / (sum_data - data[15]) * 100
        if m == 0:
            result.append('0')
        else:
            result.append(str(data[i]) + '/' + str(sum_data - data[15]) + str('(') + str("%.1f" % m) + str('%)'))
    m = data[15] / sum_data * 100
    if m == 0:
        result.append('0')
    else:
        result.append(str(data[15]) + str('(') + str("%.1f" % m) + str('%)'))
    for i in range(16, 18 + 1):  # 状态
        m = data[i] / (sum_data - data[19]) * 100
        if m == 0:
            result.append('0')
        else:
            result.append(str(data[i]) + '/' + str(sum_data - data[19]) + str('(') + str("%.1f" % m) + str('%)'))
    m = data[19] / sum_data * 100
    if m == 0:
        result.append('0')
    else:
        result.append(str(data[19]) + str('(') + str("%.1f" % m) + str('%)'))
    result.append(data[20])  # 人数
    for i in range(21, 28 + 1):
        m = data[i] / (sum_data - data[29]) * 100
        if m == 0:
            result.append('0')
        else:
            result.append(str(data[i]) + '/' + str(sum_data - data[29]) + str('(') + str("%.1f" % m) + str('%)'))
    m = data[29] / sum_data * 100
    if m == 0:
        result.append('0')
    else:
        result.append(str(data[29]) + str('(') + str("%.1f" % m) + str('%)'))
    # 性别
    for i in range(30, 32 + 1):
        m = data[i] / (sum_data - data[33]) * 100
        if m == 0:
            result.append('0')
        else:
            result.append(str(data[i]) + '/' + str(sum_data - data[33]) + str('(') + str("%.1f" % m) + str('%)'))
    m = data[33] / sum_data * 100
    if m == 0:
        result.append('0')
    else:
        result.append(str(data[33]) + str('(') + str("%.1f" % m) + str('%)'))
    # 年龄
    for i in range(34, 39 + 1):
        m = data[i] / (sum_data - data[40]) * 100
        if m == 0:
            result.append('0')
        else:
            result.append(str(data[i]) + '/' + str(sum_data - data[40]) + str('(') + str("%.1f" % m) + str('%)'))
    m = data[40] / sum_data * 100
    if m == 0:
        result.append('0')
    else:
        result.append(str(data[40]) + str('(') + str("%.1f" % m) + str('%)'))

    for i in range(41, 43 + 1):
        m = data[i] / sum_data * 100
        if m == 0:
            result.append('0')
        else:
            result.append(str(data[i]) + str('(') + str("%.1f" % m) + '%)')

    for i in range(44, 47 + 1):
        m = data[i] / (sum_data - data[48]) * 100
        if m == 0:
            result.append('0')
        else:
            result.append(str(data[i]) + '/' + str(sum_data - data[48]) + str('(') + str("%.1f" % m) + str('%)'))
    m = data[48] / sum_data * 100
    if m == 0:
        result.append('0')
    else:
        result.append(str(data[48]) + str('(') + str("%.1f" % m) + str('%)'))

    #    result_one = []
    #    for i in range(len(result)):
    #        if i != 19 and data[i] != 0:
    #            result_one.append(str(data[i]) + str('(') + str("%.2f" % result[i]*100) + str('%)'))
    #        elif i != 19 and data[i] == 0:
    #            result_one.append('0(0)')
    #        else:
    #            result_one.append(data[i])
    return result


def get_blind_radio_table(from_excel, to_excel):
    data = pd.read_excel(from_excel, index_col=0)
    data_radio = pd.DataFrame(data)
    for column in list(data.columns):
        data_column = list(data[column])
        result = get_blind_radio(data_column)
        data_radio[column] = result
    data.to_excel(to_excel)
