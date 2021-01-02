import pandas as pd
from src.data_visiable import draw_picture

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


# -------------------机构情况----------------------
def draw_indicator_top10(data_file_name, y_list, to_file_name, svg_name, y_name, pos_left="25%"):
    """
    画 某某东西 的top10条形图
    :param y_name:
    :param y_list: y轴名称（第一个是x，第二个是y）
    :param svg_name:
    :param data_file_name:
    :param to_file_name:
    :return:
    """
    data = pd.read_excel(data_file_name).head(10)

    index = list(data.index)
    index.reverse()
    data = data.loc[index]
    data = data[y_list]
    result = {}
    for data_one in y_list[1:]:
        result[data_one] = list(data[data_one])
    draw_picture.draw_bar_reverse_picture(list(data[y_list[0]]), result, to_file_name, '', svg_name, False, y_name,
                                          pos_left)


def draw_indicator_month_link(data_file_name, to_file, svg_name, stack, month_number, y_name, pos_right, width='800px', is_org=True):
    """
    画 某个指标（国家，介入手段等等）折线图和河流图
    和together的区别是 标签在右边
    :param width:
    :param pos_right:
    :param data_file_name:
    :param to_file:
    :param svg_name:
    :param stack: boolean 是否是堆叠（堆叠同时会加面积进去）
    :param month_number: 要到第几个月
    :param y_name: y轴名称
    :return:
    """
    data = pd.read_excel(data_file_name, index_col=0)
    month_list = [str(i) for i in range(1, month_number + 1)]
    data = data[month_list]
    data.index = [str(i) for i in list(data.index)]
    result = {}
    if is_org:
        month_json = {'1': 'Jan.', '2': 'Feb.', '3': 'Mar.', '4': 'Apr.', '5': 'May', '6': 'June', '7': 'July',
                      '8': 'Aug.',
                      '9': 'Sept.', '10': 'Oct.', '11': 'Nov.', '12': 'Dec.'}
        data.columns = list(month_json.values())
        org_dict = get_org_standard_file()
        org_list = [org_dict[i] for i in list(data.index)]
        data.index = org_list
    else:
        pass
    for index in list(data.index):
        result[index] = list(data.loc[index])

    draw_picture.draw_line_picture_right_legend(list(data.columns), result, to_file, '', svg_name, stack, y_name,
                                                pos_right, width)


def draw_indicator_month_river(data_file_name, to_file, svg_name, month_number, pos_right, width='800px'):
    """
    画 某个指标（国家，介入手段等等）主题河流图
        和together的区别是 标签在右边
    :param width:
    :param pos_right:
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
    data = data[month_list]
    data.index = [str(i) for i in list(data.index)]
    result = []
    for index in list(data.index):
        for column in month_list:
            result.append([xaxis_data[int(column)-1], int(data.loc[index, column]), index])
            # result.append([str(column, int(data.loc[index, column]), index])
    draw_picture.draw_river_picture_right_legend(list(data.index), result, to_file, svg_name, pos_right, width)


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
    country_list = list(data.index)
    country_standard_dict = get_org_standard_file()
    country_en = [country_standard_dict[i] for i in country_list]
    if is_type:
        index_en_dict = {'中医药': 'Traditional \nchinese\n medcine', '药物': 'Chemical \nagents \nand drugs',
                         '疫苗': 'Vaccines',
                         '瑜伽': 'Yoga', '其他手段': 'Others'}
    else:
        month_list = [str(i) for i in range(0, 6 + 1)]
        data = data[month_list]
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


def draw_indicator_country_subject_scatter(data_file_name, to_file, size, y_name):
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
    country_list = list(data.columns)
    country_standard_dict = get_country_standard_file()
    country_en = [country_standard_dict[i] for i in country_list]

    results = {}
    for country in country_list:
        result = []
        for type_label in list(data.index):
            i = list(data.index).index(type_label)
            ii = list(data.index).index(type_label)
            j = country_list.index(country)
            result.append([j, ii, float(data.iloc[j, i])])
        results[country] = result

    draw_picture.draw_triple_number_scatter(country_en, list(data.index), results, to_file, size, y_name)


def draw_indicator_country_bar(data_file_name, to_file, svg_name, stack, y_name, reverse=False, pos_right='30%'):
    """
    画 某个指标（国家，介入手段等等）柱状图
    和together的区别是 标签在右边
    :param pos_right:
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

    draw_picture.draw_bar_picture_right_legend(list(data.columns), result, to_file, '', svg_name, stack, y_name,
                                                pos_right)


def draw_indicator_country_radar(data_file_name, svg_name):
    """
    画 雷达图， index 是边， column是线
    :param data_file_name:
    :param svg_name:
    :return:
    """
    data = pd.read_excel(data_file_name, index_col=0)
    result = {}
    for index in list(data.columns):
        result[index] = list(data[index])
    # 设置indicator
    max_value = data.max(axis=1).max()
    if max_value<1:
        max_value = 1
    else:
        max_value = int(max_value/10)*10 + 10

    indicator = []
    for key in list(data.index):
        indicator.append({'text': key, 'max': max_value})
    draw_picture.draw_radar_picture(result, indicator, svg_name)


def draw_heat_map_wc(data_file_name, to_file, svg_name):
    grid_data = []  # {} ,key包括 series_name, y_name, sub_title, value
    data = pd.read_excel(data_file_name, index_col=0)
    data_columns = list(data.columns)
    data = data[data_columns]
    max_number = int(data.max().max())
    print(max_number)
    # 先获取结果数据
    grid_list = ['']
    for sub_title in grid_list:
        result = {}
        data_sub = data
        y_name = list(data_columns)
        y_name.reverse()
        result['series_name'] = sub_title
        result['sub_title'] = sub_title
        result['y_name'] = y_name
        value = []
        for y_name_one in y_name:
            for x_name_one in data_columns:
                i = data_columns.index(x_name_one)
                j = y_name.index(y_name_one)
                value.append([i, j, int(data_sub.loc[y_name_one, x_name_one])])
        result['value'] = value
        grid_data.append(result)
    draw_picture.draw_heat_map_picture(grid_data, data_columns[2:], max_number, to_file, svg_name, '600px')
