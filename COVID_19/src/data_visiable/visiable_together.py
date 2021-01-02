import pandas as pd
from src.data_visiable import draw_picture
from snapshot_phantomjs import snapshot
from pyecharts.render import make_snapshot


# TODO： 获取字典
def get_country_standard_file():
    country_standard_file = 'D:\\zyx-project\\paper\\python_paper\\analysis_result\\国家映射标准格式.xlsx'
    country_standard_data = pd.read_excel(country_standard_file)
    country_standard_dict = {}
    for index, row in country_standard_data.iterrows():
        country_standard_dict[row['国家'].strip()] = row['标准'].strip()
    return country_standard_dict


def get_org_standard_file():
    country_standard_file = 'D:\\zyx-project\\paper\\python_paper\\analysis_result\\机构映射标准格式.xlsx'
    country_standard_data = pd.read_excel(country_standard_file)
    country_standard_dict = {}
    for index, row in country_standard_data.iterrows():
        country_standard_dict[row['机构'].strip()] = row['标准'].strip()
    return country_standard_dict


def get_cluster_standard_file():
    country_standard_file = 'D:\\zyx-project\\paper\\python_paper\\analysis_result\\聚类结果.xlsx'
    country_standard_data = pd.read_excel(country_standard_file)
    country_standard_dict = {}
    for index, row in country_standard_data.iterrows():
        country_standard_dict[str(row['类别']).strip()] = str(row['name']).strip()
    return country_standard_dict


# -------------------总体情况----------------------
def draw_over_all_with_patient(data_file_name, to_file_name, svg_name):
    """
    每月 成果数，感染人数
    :param svg_name:
    :param data_file_name:
    :param to_file_name:
    :return:
    """
    data = pd.read_excel(data_file_name)
    draw_picture.draw_line_with_two_y(list(data['month']), 'paper', list(data['paper_number']), 'trail',
                                      list(data['trail_number']), 'infections', list(data['新增量']),
                                      'achievements/No.', 'infections/No.', to_file_name, '', svg_name)


def draw_over_all_with_radio(data_file_name, to_file_name, svg_name):
    """
     每月 成果数，感染人数增长率
     :param svg_name:
     :param data_file_name:
     :param to_file_name:
     :return:
     """
    data = pd.read_excel(data_file_name)
    draw_picture.draw_line_with_two_y(list(data['month']), 'paper', list(data['paper_number']), 'trial',
                                      list(data['trail_number']), 'infections rate', list(data['增长率']),
                                      'achievements/No.', 'infections rate(%)', to_file_name, '', svg_name)


# -------------------国家情况----------------------
def draw_country_number(dict_file, number_excel, to_file, svg_name, label_name):
    """
    :param dict_file: 字典名称
    :param number_excel:
    :param to_file:
    :param svg_name:
    :param label_name: 图例的名称
    :return:
    """
    # 字典
    country_data = pd.read_excel(dict_file)
    country_dict = {}
    for index, row in country_data.iterrows():
        country_dict[row['country']] = row['en']

    # 数据
    number_data = pd.read_excel(number_excel)
    number_data = number_data[~ (number_data['country'].isin(['europe', 'non-europe']))]
    number_max = int((int(number_data['number'].astype(int).max()) / 100 + 1)) * 100
    # number_max = 500
    print(number_max)
    result = []
    for index, row in number_data.iterrows():
        if country_dict.__contains__(row['country']):
            result.append([country_dict[row['country']], int(row['number'])])
        else:
            result.append([row['country'], int(row['number'])])
    # 画图
    draw_picture.draw_map_world(result, to_file, svg_name, label_name, number_max)


def draw_country_rank_change(data_file_name, to_file, svg_name):
    """
    国家排名
    :param data_file_name:
    :param to_file:
    :param svg_name:
    :return:
    """
    data = pd.read_excel(data_file_name)
    data['rank'] = list(range(1, 31))
    data_country = data.sort_values(by='number', ascending=False)
    data_country = list(data_country.drop_duplicates(subset=['country'])['country'])
    axis_name_list = ['rank of papers', 'rank of trials', 'rank of achievements']
    axis_data = [str(i) for i in range(1, 11)] + ['10+']
    results = []
    country_standard_dict = get_country_standard_file()
    for country in data_country:
        result = []
        for type_label in ['论文', '试验', '一起']:
            if len(data[(data['country'] == country) & (data['type'] == type_label)]) > 0:
                rank = int(list(data[(data['country'] == country) & (data['type'] == type_label)]['rank'])[0]) % 10
                if rank == 0:
                    rank = 10
                result.append(str(rank))
            else:
                result.append(axis_data[-1])
        results.append([country_standard_dict[country], [result]])
    draw_picture.draw_rank_change(axis_name_list, axis_data, results, to_file, svg_name)


def draw_country_rank_change_scatter(data_file_name, to_file):
    data = pd.read_excel(data_file_name)
    data['rank'] = list(range(1, 31))
    data_country = data.sort_values(by='number', ascending=False)
    data_country = list(data_country.drop_duplicates(subset=['country'])['country'])
    axis_name_list = ['rank of papers', 'rank of trails', 'rank of achievements']
    axis_data = [str(i) for i in range(1, 11)]
    results = {}
    for country in data_country:
        result = []
        for type_label in ['论文', '试验', '一起']:
            if len(data[(data['country'] == country) & (data['type'] == type_label)]) > 0:
                rank = int(list(data[(data['country'] == country) & (data['type'] == type_label)]['rank'])[0]) % 10
                num = int(list(data[(data['country'] == country) & (data['type'] == type_label)]['number'])[0])
                if rank == 0:
                    rank = 10
                i = ['论文', '试验', '一起'].index(type_label)
                j = axis_data.index(str(rank))
                result.append([j, i, num])
        results[country] = result
    draw_picture.draw_triple_rank_scatter(axis_name_list, axis_data, results, to_file)


def draw_indicator_month_link(data_file_name, to_file, svg_name, stack, month_number, y_name, is_intervention=True):
    """
    画 某个指标（国家，介入手段等等）折线图和河流图
    :param label_right:
    :param data_file_name:
    :param to_file:
    :param svg_name:
    :param stack: boolean 是否是堆叠（堆叠同时会加面积进去）
    :param month_number: 要到第几个月
    :param y_name: y轴名称
    :return:
    """
    data = pd.read_excel(data_file_name, index_col=0)
    data = data
    data.index = [str(i) for i in list(data.index)]
    result = {}
    if is_intervention:
        index_en_dict = {'中医药': 'Traditional chinese medcine', '药物': 'Chemical agents and drugs', '疫苗': 'Vaccines',
                         '瑜伽': 'Yoga', '其他手段': 'Others'}
        for index in list(index_en_dict.keys()):
            result[index_en_dict[index]] = list(data.loc[index])
    else:
        for index in list(data.index):
            result[index] = list(data.loc[index])
    draw_picture.draw_line_picture(list(data.columns), result, to_file, '', svg_name, stack, y_name)


def draw_indicator_month_river(data_file_name, to_file, svg_name, month_number, is_country=True):
    """
    画 某个指标（国家，介入手段等等）主题河流图
    :param data_file_name:
    :param to_file:
    :param svg_name:
    :param month_number: 要到第几个月
    :return:
    """
    xaxis_data = ['2020-01-31', '2020-02-29', '2020-03-31', '2020-04-30', '2020-05-31', '2020-06-30', '2020-07-31',
                  '2020-08-31', '2020-09-30', '2020-10-31', '2020-11-30', '2020-12-31']
    data = pd.read_excel(data_file_name, index_col=0)
    month_list = [str(i) for i in range(1, month_number + 1)]
    data.columns = month_list
    if is_country:
        index_dict = get_country_standard_file()
        data.index = [index_dict[str(i)] for i in list(data.index)]
    else:
        data.sort_index(inplace=True)
        index_dict = get_cluster_standard_file()
        data.index = [index_dict[str(i)] for i in list(data.index)]
    result = []
    for index in list(data.index):
        for column in month_list:
            result.append([xaxis_data[int(column) - 1], int(data.loc[index, column]), index])
            # result.append([str(column, int(data.loc[index, column]), index])
    draw_picture.draw_river_picture(list(data.index), result, to_file, svg_name)


def draw_indicator_month_scatter(data_file_name, to_file, month_number, size, y_name, is_org=True):
    """
    某个指标（国家，介入手段等等）每月发文量

    :param data_file_name:
    :param to_file:
    :param month_number:
    :param size:
    :param y_name:
    :return:
    """
    data = pd.read_excel(data_file_name, index_col=0)
    month_list = [str(i) for i in range(1, month_number + 1)]
    data = data[month_list]
    country_list = list(data.index)
    results = {}
    for country in country_list:
        result = []
        for type_label in month_list:
            i = month_list.index(type_label)
            j = country_list.index(country)
            result.append([j, i, int(data.iloc[j, i])])
        results[country] = result
    month_json = {'1': 'Jan.', '2': 'Feb.', '3': 'Mar.', '4': 'Apr.', '5': 'May', '6': 'June', '7': 'July',
                  '8': 'Aug.',
                  '9': 'Sept.', '10': 'Oct.', '11': 'Nov.', '12': 'Dec.'}
    month_list = list(month_json.values())
    if is_org:
        org_dict = get_org_standard_file()
        org_list = [org_dict[i] for i in list(data.index)]
    else:
        org_list = list(data.index)
    draw_picture.draw_triple_number_scatter(month_list, org_list, results, to_file, size, y_name)


def draw_indicator_month_rank(data_file_name):
    """
    每月的排名情况，
    :param data_file_name:
    :return:
    """
    data = pd.read_excel(data_file_name)
    # data['rank'] = list(range(1, 31))
    # data_country = data.sort_values(by='number', ascending=False)
    # data_country = list(data_country.drop_duplicates(subset=['country'])['country'])
    # axis_name_list = ['paper', 'trail', 'achievements']
    # axis_data = [str(i) for i in range(1, 11)] + ['10+']
    # results = []
    # for country in data_country:
    #     result = []
    #     for type_label in ['论文', '试验', '一起']:
    #         if len(data[(data['country'] == country) & (data['type'] == type_label)]) > 0:
    #             rank = int(list(data[(data['country'] == country) & (data['type'] == type_label)]['rank'])[0]) % 10
    #             if rank == 0:
    #                 rank = 10
    #             result.append(str(rank))
    #         else:
    #             result.append(axis_data[-1])
    #     results.append([country, [result]])
    # draw_picture.draw_rank_change(axis_name_list, axis_data, results, to_file, svg_name)


# -------------------介入手段, 层次聚类情况----------------------
def draw_overall_type_bar(data_file_name, to_file, svg_name, stack, y_name, y_list, reverse, is_type=True):
    """
    :param is_type: 是介入手段
    :param data_file_name:
    :param to_file:
    :param svg_name:
    :param stack:
    :param y_name:
    :param y_list:
    :param reverse: 数据是否转置
    :return:
    """
    data = pd.read_excel(data_file_name, index_col=0)
    data = data[y_list]
    data.index = [str(i) for i in list(data.index)]
    index_en_dict = {'中医药': 'Traditional \nchinese medcine', '药物': 'Chemical agents \nand drugs', '疫苗': 'Vaccines',
                     '瑜伽': 'Yoga', '其他手段': 'Others'}
    if not is_type:
        index_en_dict = get_cluster_standard_file()
    if reverse:
        data = pd.DataFrame(data.values.T, index=data.columns, columns=data.index)
        data.columns = [index_en_dict[i] for i in list(data.columns)]
        data = data[list(index_en_dict.values())]
    result = {}
    for index in list(data.index):
        result[index] = list(data.loc[index])

    draw_picture.draw_bar_picture(list(data.columns), result, to_file, '', svg_name, stack, y_name)


def draw_overall_type_pie(data_file_name, to_file, svg_name, y_list, color=None):
    """
    :param color: [str], 颜色列表
    :param data_file_name:
    :param to_file:
    :param svg_name:
    :param y_list:
    :return:
    """
    data = pd.read_excel(data_file_name, index_col=0)
    data = data[y_list]
    result = []
    for index in list(data.index):
        for column in y_list:
            result.append((str(column) + '-' + str(index), int(data.loc[index, column])))
    draw_picture.draw_pie_picture(result, to_file, svg_name, color)


def draw_indicator_country_scatter(data_file_name, to_file, size, y_name, is_type=True):
    """
    某个指标（介入手段等等）top10国家发文量
    :param data_file_name:
    :param to_file:
    :param month_number:
    :param size:
    :param y_name:
    :return:
    """
    data = pd.read_excel(data_file_name, index_col=0)
    data = data
    country_list = list(data.index)
    country_standard_dict = get_country_standard_file()
    country_en = [country_standard_dict[i] for i in country_list]
    if is_type:
        index_en_dict = {'中医药': 'Traditional \nchinese\n medcine', '药物': 'Chemical \nagents \nand drugs',
                         '疫苗': 'Vaccines',
                         '瑜伽': 'Yoga', '其他手段': 'Others'}
    else:
        index_en_dict = get_cluster_standard_file()
    results = {}
    for country in country_list:
        result = []
        for type_label in list(index_en_dict.keys()):
            i = list(data.columns).index(type_label)
            ii = list(index_en_dict.keys()).index(type_label)
            j = country_list.index(country)
            result.append([j, ii, float(data.iloc[j, i])])
        results[country] = result

    draw_picture.draw_triple_number_scatter(list(index_en_dict.values()), country_en, results, to_file, size, y_name)


def draw_drug_number_table(paper_number_excel, trail_number_excel, all_number_excel, result_table):
    paper_data = pd.read_excel(paper_number_excel)
    trail_data = pd.read_excel(trail_number_excel)
    all_data = pd.read_excel(all_number_excel)
    result_data = pd.DataFrame()
    result_data['论文'] = paper_data.apply(lambda x: x['drug'] + '(' + str(x['number']) + ')', axis=1)
    result_data['试验'] = trail_data.apply(lambda x: x['drug'] + '(' + str(x['number']) + ')', axis=1)
    result_data['一起'] = all_data.apply(lambda x: x['drug'] + '(' + str(x['number']) + ')', axis=1)
    result_data['rank'] = list(range(1, len(result_data + 1)))
    result_data.to_excel(result_table, index=None)


def draw_drug_month_table(paper_number_excel, trail_number_excel, all_number_excel, result_table):
    paper_data = pd.read_excel(paper_number_excel)
    trail_data = pd.read_excel(trail_number_excel)
    all_data = pd.read_excel(all_number_excel)
    result_data = pd.DataFrame()
    month = list(range(1, 13))
    result_data['month'] = month
    # 论文
    paper_result_1 = []
    trail_result_1 = []
    all_result_1 = []
    for month_one in month:
        paper_result = []
        trail_result = []
        all_result = []
        # 论文
        paper_data_sub = paper_data[paper_data['month'] == month_one]
        for index, row in paper_data_sub.iterrows():
            paper_result.append(row['drug'] + '(' + str(row['number']) + ')')
        # 试验
        trail_data_sub = trail_data[trail_data['month'] == month_one]
        for index, row in trail_data_sub.iterrows():
            trail_result.append(row['drug'] + '(' + str(row['number']) + ')')
        # 一起
        all_data_sub = all_data[all_data['month'] == month_one]
        for index, row in all_data_sub.iterrows():
            all_result.append(row['drug'] + '(' + str(row['number']) + ')')
        paper_result_1.append('\n'.join(paper_result))
        trail_result_1.append('\n'.join(trail_result))
        all_result_1.append('\n'.join(all_result))

    result_data['论文'] = paper_result_1
    result_data['试验'] = trail_result_1
    result_data['一起'] = all_result_1
    result_data.to_excel(result_table, index=None)


def draw_drug_country_table(paper_number_excel, trail_number_excel, all_number_excel, result_table):
    paper_data = pd.read_excel(paper_number_excel)
    trail_data = pd.read_excel(trail_number_excel)
    all_data = pd.read_excel(all_number_excel)
    result_data = pd.DataFrame()
    month = list(paper_data['country'].drop_duplicates())
    result_data['country'] = month
    # 论文
    paper_result_1 = []
    trail_result_1 = []
    all_result_1 = []
    for month_one in month:
        paper_result = []
        trail_result = []
        all_result = []
        # 论文
        paper_data_sub = paper_data[paper_data['country'] == month_one]
        for index, row in paper_data_sub.iterrows():
            paper_result.append(row['drug'] + '(' + str(row['number']) + ')')
        # 试验
        trail_data_sub = trail_data[trail_data['country'] == month_one]
        for index, row in trail_data_sub.iterrows():
            trail_result.append(row['drug'] + '(' + str(row['number']) + ')')
        # 一起
        all_data_sub = all_data[all_data['country'] == month_one]
        for index, row in all_data_sub.iterrows():
            all_result.append(row['drug'] + '(' + str(row['number']) + ')')
        paper_result_1.append('\n'.join(paper_result))
        trail_result_1.append('\n'.join(trail_result))
        all_result_1.append('\n'.join(all_result))

    result_data['论文'] = paper_result_1
    result_data['试验'] = trail_result_1
    result_data['一起'] = all_result_1
    result_data.to_excel(result_table, index=None)


def draw_indicator_country_bar(data_file_name, to_file, svg_name, stack, y_name, reverse=False):
    """
    画 某个指标（国家，介入手段等等）柱状图
    :param reverse:
    :param data_file_name:
    :param to_file:
    :param svg_name:
    :param stack: boolean 是否是堆叠（堆叠同时会加面积进去）
    :param month_number: 要到第几个月
    :param y_name: y轴名称
    :return:
    """
    data = pd.read_excel(data_file_name, index_col=0)
    if reverse:
        data = pd.DataFrame(data.values.T, index=data.columns, columns=data.index)
    result = {}
    for index in list(data.index):
        result[index] = list(data.loc[index])

    draw_picture.draw_bar_picture(list(data.columns), result, to_file, '', svg_name, stack, y_name)
