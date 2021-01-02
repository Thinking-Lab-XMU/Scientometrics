import pandas as pd
from src.data_visiable import draw_picture


# -------------------注册平台情况----------------------
def draw_tree_picture(data_file_name, y_list, to_file_name, svg_name):
    """
    画  树图
    :param y_list: y轴名称（第一个是name，第二个是value）
    :param svg_name:
    :param data_file_name:
    :param to_file_name:
    :return:
    """
    data = pd.read_excel(data_file_name)
    data = data[y_list]
    result = []
    for index in list(data.index):
        result.append({'value': int(data.loc[index, y_list[1]]), 'name': data.loc[index, y_list[0]]})
    draw_picture.draw_tree_picture(result, to_file_name, svg_name)


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
            result.append((str(index), int(data.loc[index, column])))
    draw_picture.draw_pie_picture(result, to_file, svg_name, color)


def draw_heat_map_grid(data_file_name, to_file, svg_name):
    grid_data = []  # {} ,key包括 series_name, y_name, sub_title, value
    data = pd.read_excel(data_file_name)
    data = data.fillna('N/A')
    data_columns = list(data.columns)
    # data_columns.remove('Global')
    # data_columns.remove('non-eu')
    # data_columns.remove('europe')
    data = data[data_columns]
    max_number = int(data[data_columns[2:]].max().max())
    print(max_number)
    # 先获取结果数据
    grid_list = list(data['name'].drop_duplicates())
    for sub_title in grid_list:
        result = {}
        data_sub = data[data['name'] == sub_title]
        data_sub.index = data_sub['type']
        y_name = list(data_sub['type'])
        data_sub = data_sub[data_columns[2:]]
        result['series_name'] = sub_title
        result['sub_title'] = sub_title
        result['y_name'] = y_name
        value = []
        for y_name_one in y_name:
            for x_name_one in data_columns[2:]:
                i = data_columns[2:].index(x_name_one)
                j = y_name.index(y_name_one)
                value.append([i, j, int(data_sub.loc[y_name_one, x_name_one])])
        result['value'] = value
        grid_data.append(result)
    draw_picture.draw_heat_map_picture(grid_data, data_columns[2:], 408, to_file, svg_name)
