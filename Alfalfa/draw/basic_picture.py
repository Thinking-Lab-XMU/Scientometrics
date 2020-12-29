# -*- coding:utf-8 -*-
# @Time    : 2020/10/15 11:30
# @Author  : zhy


'''
小论文中基础的图
'''


import pyecharts.options as opts
from pyecharts.charts import Line
from pyecharts.charts import Bar,Grid, Map, ThemeRiver, Radar, HeatMap, Scatter, Graph
from pyecharts.faker import Faker
import numpy as np



save_root = "D:/draw/pictures/"
# relationship_color = ['#c23531','#2f4554', '#61a0a8', '#d48265', '#91c7ae','#749f83',  '#ca8622', '#bda29a','#6e7074']  # 9种

# 2-每年发文量（折线图）
def fawenliang_per_year():

    x_data = [str(i) for i in range(2009, 2021)]
    # x_data[len(x_data)-1] = x_data[len(x_data)-1] + ".8.14"
    y_data = [370, 364, 390, 349, 431, 425, 404, 438, 450, 500, 527, 363]


    (
        Line(init_opts=opts.InitOpts(width="1000px", height="500px", page_title="每年发文量", bg_color="white"))
            .set_global_opts(
            toolbox_opts=opts.ToolboxOpts(),
            # tooltip_opts=opts.TooltipOpts(is_show=False),
            # title_opts=opts.TitleOpts(title="Number of articles published per year", pos_left="35%"),
            xaxis_opts=opts.AxisOpts(type_="category", name="Year",
                                     name_textstyle_opts=opts.TextStyleOpts(font_size=15),
                                     axistick_opts=opts.AxisTickOpts(is_align_with_label=True)),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
                max_=600,
                min_=300,
            ),
            legend_opts=opts.LegendOpts(pos_left="90%", pos_top="10%")
        )
            .add_xaxis(xaxis_data=x_data)
            .add_yaxis(
            series_name="Number",
            y_axis=y_data,
            symbol="emptyCircle",
            symbol_size=10,
            linestyle_opts = opts.LineStyleOpts(width=5, opacity=0.6),
            label_opts=opts.LabelOpts(position="top",font_size=15, margin=15)
        )
            .render(save_root + "2-每年发文量.html")
    )


# 31-前十期刊发文量（柱状图）
def top_10_journal():

    x_data = ["FRONTIERS IN PLANT SCIENCE", "JOURNAL OF DAIRY SCIENCE", "PLOS ONE", "NEW PHYTOLOGIST",
              "CROP & PASTURE SCIENCE", "PLANT AND SOIL", "AGRONOMY JOURNAL", "ANIMAL FEED SCIENCE AND TECHNOLOGY",
              "CROP SCIENCE", "PLANT PHYSIOLOGY"]
    y_data = [120, 92, 91, 78, 71, 69, 66, 64, 60, 57]
    grid = Grid()
    c = (
        Bar(init_opts=opts.InitOpts(width="1000px", height="500px", page_title="前十期刊发文量", bg_color="white"))
            .add_xaxis(x_data)
            .add_yaxis("Number", y_data, bar_width='60%', itemstyle_opts=opts.ItemStyleOpts(opacity=0.8))
            .set_global_opts(
                toolbox_opts=opts.ToolboxOpts(),
                # title_opts=opts.TitleOpts(title="Top 10 Journals", pos_left='42%'),
                xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(position="left", rotate=30, font_size=10),
                                         axistick_opts=opts.AxisTickOpts(is_align_with_label=True)),
                yaxis_opts=opts.AxisOpts(max_=150),
                legend_opts=opts.LegendOpts(pos_left="85%", pos_top="10%")
                # datazoom_opts=opts.DataZoomOpts(pos_bottom='2%'),
        )
            # .render(save_root + "2-前十期刊发文量.html")
    )
    grid.add(c, grid_opts=opts.GridOpts(pos_bottom="40%", pos_left='15%'))
    grid.render(save_root + "31-前十期刊发文量.html")


# 32-发文量前5期刊（折线图，多条）
def top_5_journal_per_year():
    x_data = [str(i) for i in range(2009, 2021)]
    y_data_1 = [0, 0, 0, 3, 7, 7, 14, 24, 21, 22, 14, 8]   # FRONTIERS IN PLANT SCIENCE
    y_data_2 = [11, 8, 5, 8, 12, 9, 7, 8, 7, 7, 6, 4]    # JOURNAL OF DAIRY SCIENCE
    y_data_3 = [0, 1, 2, 6, 16, 17, 12, 7, 14, 10, 4, 2]    # PLOS ONE
    y_data_4 = [4, 3, 8, 7, 9, 8, 4, 4, 5, 6, 10, 10]    # NEW PHYTOLOGIST
    y_data_5 = [7, 10, 6, 12, 3, 5, 5, 5, 8, 6, 2, 2]    # CROP & PASTURE SCIENCE

    c = (
        Line(init_opts=opts.InitOpts(width="1000px", height="500px", page_title="发文量前5期刊的每年发文量", bg_color="white"))
            .set_global_opts(
            toolbox_opts=opts.ToolboxOpts(),
            # tooltip_opts=opts.TooltipOpts(is_show=False),
            # title_opts=opts.TitleOpts(title="Number of papers published in top 5 journals per year", pos_left="25%"),
            xaxis_opts=opts.AxisOpts(type_="category", name="Year",
                                     name_textstyle_opts=opts.TextStyleOpts(font_size=15),
                                     axistick_opts=opts.AxisTickOpts(is_align_with_label=True)),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
                max_=25,
            ),
            legend_opts=opts.LegendOpts( pos_top="95%")
        )
            .add_xaxis(xaxis_data=x_data)
            .add_yaxis(
            series_name="1-FRONTIERS IN PLANT SCIENCE",
            y_axis=y_data_1,
            symbol="emptyCircle",
            symbol_size=5,
            linestyle_opts = opts.LineStyleOpts(width=5, opacity=0.6),
            label_opts=opts.LabelOpts(is_show=False),
            markpoint_opts=opts.MarkPointOpts(
                data=[
                    opts.MarkPointItem(type_="max", name="最大值"),
                ],
            ),
        )
            .add_yaxis(
            series_name="2-JOURNAL OF DAIRY SCIENCE",
            y_axis=y_data_2,
            symbol="emptyCircle",
            symbol_size=5,
            linestyle_opts = opts.LineStyleOpts(width=5, opacity=0.6),
            label_opts=opts.LabelOpts(is_show=False),
            markpoint_opts=opts.MarkPointOpts(
                data=[
                    opts.MarkPointItem(type_="max", name="最大值"),
                ],
            ),
        )
            .add_yaxis(
            series_name="3-PLOS ONE",
            y_axis=y_data_3,
            symbol="emptyCircle",
            symbol_size=5,
            linestyle_opts = opts.LineStyleOpts(width=5, opacity=0.6),
            label_opts=opts.LabelOpts(is_show=False),
            markpoint_opts=opts.MarkPointOpts(
                data=[
                    opts.MarkPointItem(type_="max", name="最大值"),
                ],
            ),
        )
            .add_yaxis(
            series_name="4-NEW PHYTOLOGIST",
            y_axis=y_data_4,
            symbol="emptyCircle",
            symbol_size=5,
            linestyle_opts = opts.LineStyleOpts(width=5, opacity=0.6),
            label_opts=opts.LabelOpts(is_show=False),
            markpoint_opts=opts.MarkPointOpts(
                data=[
                    opts.MarkPointItem(type_="max", name="最大值"),
                ],
            ),
        )
            .add_yaxis(
            series_name="5-CROP & PASTURE SCIENCE",
            y_axis=y_data_5,
            symbol="emptyCircle",
            symbol_size=5,
            linestyle_opts = opts.LineStyleOpts(width=5, opacity=0.6),
            label_opts=opts.LabelOpts(is_show=False),
            markpoint_opts=opts.MarkPointOpts(
                data=[
                    opts.MarkPointItem(type_="max", name="最大值"),
                ],
            ),
            # label_opts=opts.LabelOpts(position="top",font_size=15, margin=15)
        )
            .render(save_root + "32-发文量前5期刊的每年发文量.html")
    )


# 41-所有国家发文量，分档（地图）
def country_all():
    x = ["United States", "China", "France", "Australia", "Canada", "Spain", "Iran", "Italy", "Germany", "Poland",
         "United Kingdom", "Turkey", "Tunisia", "New Zealand", "Argentina", "Mexico", "Brazil", "Japan", "India", "Portugal",
         "Saudi Arabia", "Belgium", "Korea", "Egypt", "Czech Rep.", "Netherlands", "Switzerland", "Hungary",
         "Denmark", "Greenland", "Serbia", "Russia", "Pakistan", "Morocco", "South Africa", "Sweden", "Chile", "Greece", "Romania",
         "Austria", "Bulgaria", "Croatia", "Lithuania", "Algeria", "Israel", "Uruguay", "Taiwan", "Luxembourg",
         "Slovakia", "Bangladesh", "Slovenia", "Cyprus", "Ireland", "Oman", "Thailand", "Finland", "Jordan",
         "Malaysia", "Sudan", "Norway", "Syria", "Vietnam", "Ukraine", "Bosnia and Herz.", "Estonia", "Kenya",
         "Lebanon", "Libya", "Cuba", "Ethiopia", "Nigeria", "Peru", "Colombia", "Ecuador", "Ghana", "Kuwait",
         "Kyrgyzstan", "Mauritius", "Philippines", "Senegal", "Togo", "Zimbabwe", "Belarus", "Burkina Faso",
         "Costa Rica", "Indonesia", "Iraq", "Kazakhstan", "Kosovo", "Latvia", "Lesotho", "Macedonia", "Malawi",
         "Malta", "Namibia", "Paraguay", "Qatar", "Dem. Rep. Congo", "Tanzania", "United Arab Emirates", "Uganda", "Venezuela"]
    y = [1215, 1146, 486, 328, 293, 290, 256, 218, 186, 143, 141, 137, 128, 109, 104, 100, 88, 82, 80, 78, 77, 69,
         69, 60, 56, 51, 51, 49, 48, 48,  47, 43, 41, 38, 33, 33, 32, 31, 31, 30, 29, 17, 17, 16, 14, 14, 12, 10, 10,
         9, 9, 8, 8, 8, 8, 7, 7, 7, 7, 6, 6, 6, 5, 4, 4, 4, 4, 4, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1,
         1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

    c = (
        Map(init_opts=opts.InitOpts(width="1200px", height="600px", page_title="国家发文量", bg_color="white"))
            .add("", [list(z) for z in zip(x, y)], maptype="world", is_map_symbol_show=False,
                 label_opts=opts.LabelOpts())
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(
                toolbox_opts=opts.ToolboxOpts(),
                # title_opts=opts.TitleOpts(title="国家发文量"),
                visualmap_opts=opts.VisualMapOpts(max_=1250,  is_piecewise=True,# range_color=['#D7DA8B', '#E15457'],
                                                  pieces=[{"min":291, "max":1250}, {"min":141, "max":290},
                                                          {"min":101, "max":140}, {"min":31, "max":100},
                                                          {"min":1, "max":30}], pos_left="10%"),
        )
            .render(save_root + "41-国家发文量.html")
    )


# 42-发文量前十国家的发文量（柱状图）
def top_10_country():
    x_data = ["USA", "China", "France", "Australia", "Canada"]  #, "Spain", "Iran", "Italy", "Germany", "Poland"]
    y_data = [1215, 1146, 486, 328, 293] #, 290, 256, 218, 186, 143]
    grid = Grid(init_opts=opts.InitOpts(bg_color="white"))
    c = (
        Bar(init_opts=opts.InitOpts(width="800px", height="600px", page_title="前十国家发文量", bg_color="white"))
            .add_xaxis(x_data)
            .add_yaxis("Number", y_data, bar_width='60%', itemstyle_opts=opts.ItemStyleOpts(opacity=0.8))   # , itemstyle_opts=opts.ItemStyleOpts(opacity=0.8))
            .set_global_opts(
            toolbox_opts=opts.ToolboxOpts(),
            # title_opts=opts.TitleOpts(title="前十国家发文量", pos_left='50%'),
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(position="left", font_size=12),  # rotate=30,
                                     axistick_opts=opts.AxisTickOpts(is_align_with_label=True)),
            yaxis_opts=opts.AxisOpts(max_=1400),
            # legend_opts=opts.LegendOpts(pos_left="80%", pos_top="10%")
        )
    )
    grid.add(c, grid_opts=opts.GridOpts(pos_bottom="10%", pos_left='20%'))
    grid.render(save_root + "42-前十国家发文量.html")


# 43-前5发文国家每年发文量（河流图）
def top_5_country():
    x_data = ["USA", "China", "France", "Australia", "Canada", "Spain", "Iran", "Italy", "Germany", "Poland"]
    y_data = [
        # USA
        ["2009", 94, "USA"], ["2010", 94, "USA"], ["2011", 95, "USA"], ["2012", 87, "USA"],
        ["2013", 105, "USA"], ["2014", 102, "USA"], ["2015", 103, "USA"], ["2016", 95, "USA"],
        ["2017", 118, "USA"], ["2018", 127, "USA"], ["2019", 121, "USA"], ["2020", 74, "USA"],
        # China
        ["2009", 50, "China"], ["2010", 31, "China"], ["2011", 72, "China"], ["2012", 49, "China"],
        ["2013", 76, "China"], ["2014", 171, "China"], ["2015", 82, "China"], ["2016", 120, "China"],
        ["2017", 116, "China"], ["2018", 158, "China"], ["2019", 184, "China"], ["2020", 137, "China"],
        # France
        ["2009", 34, "France"], ["2010", 44, "France"], ["2011", 48, "France"], ["2012", 41, "France"],
        ["2013", 57, "France"], ["2014", 51, "France"], ["2015", 36, "France"], ["2016", 49, "France"],
        ["2017", 40, "France"], ["2018", 31, "France"], ["2019", 29, "France"], ["2020", 26, "France"],
        # Australia
        ["2009", 24, "Australia"], ["2010", 41, "Australia"], ["2011", 27, "Australia"], ["2012", 29, "Australia"],
        ["2013", 18, "Australia"], ["2014", 25, "Australia"], ["2015", 26, "Australia"], ["2016", 36, "Australia"],
        ["2017", 23, "Australia"], ["2018", 33, "Australia"], ["2019", 22, "Australia"], ["2020", 27, "Australia"],
        # Canada
        ["2009", 22, "Canada"], ["2010", 22, "Canada"], ["2011", 32, "Canada"], ["2012", 25, "Canada"],
        ["2013", 23, "Canada"], ["2014", 29, "Canada"], ["2015", 26, "Canada"], ["2016", 24, "Canada"],
        ["2017", 28, "Canada"], ["2018", 23, "Canada"], ["2019", 23, "Canada"], ["2020", 16, "Canada"],
        # # Spain
        # ["2009", 94, "Spain"], ["2010", 94, "Spain"], ["2011", 95, "Spain"], ["2012", 87, "Spain"],
        # ["2013", 105, "Spain"], ["2014", 102, "Spain"], ["2015", 103, "Spain"], ["2016", 95, "Spain"],
        # ["2017", 118, "Spain"], ["2018", 127, "Spain"], ["2019", 121, "Spain"], ["2020", 74, "Spain"],
        # # USA
        # ["2009", 94, "USA"], ["2010", 94, "USA"], ["2011", 95, "USA"], ["2012", 87, "USA"],
        # ["2013", 105, "USA"], ["2014", 102, "USA"], ["2015", 103, "USA"], ["2016", 95, "USA"],
        # ["2017", 118, "USA"], ["2018", 127, "USA"], ["2019", 121, "USA"], ["2020", 74, "USA"],
        # # USA
        # ["2009", 94, "USA"], ["2010", 94, "USA"], ["2011", 95, "USA"], ["2012", 87, "USA"],
        # ["2013", 105, "USA"], ["2014", 102, "USA"], ["2015", 103, "USA"], ["2016", 95, "USA"],
        # ["2017", 118, "USA"], ["2018", 127, "USA"], ["2019", 121, "USA"], ["2020", 74, "USA"],
        # # USA
        # ["2009", 94, "USA"], ["2010", 94, "USA"], ["2011", 95, "USA"], ["2012", 87, "USA"],
        # ["2013", 105, "USA"], ["2014", 102, "USA"], ["2015", 103, "USA"], ["2016", 95, "USA"],
        # ["2017", 118, "USA"], ["2018", 127, "USA"], ["2019", 121, "USA"], ["2020", 74, "USA"],
        # # USA
        # ["2009", 94, "USA"], ["2010", 94, "USA"], ["2011", 95, "USA"], ["2012", 87, "USA"],
        # ["2013", 105, "USA"], ["2014", 102, "USA"], ["2015", 103, "USA"], ["2016", 95, "USA"],
        # ["2017", 118, "USA"], ["2018", 127, "USA"], ["2019", 121, "USA"], ["2020", 74, "USA"],
    ]


    # 河流图
    c = (
        ThemeRiver(init_opts=opts.InitOpts(width="600px", height="400px", bg_color="white"))
            .add(
            series_name=x_data,
            data=y_data,
            singleaxis_opts=opts.SingleAxisOpts(
                pos_top="50", pos_bottom="50", type_="value", min_="2009", max_="2020"
            ),
            label_opts=opts.LabelOpts(font_size=20, position="insideLeft", distance=10, font_style="oblique")
        )
            .set_global_opts(
            toolbox_opts=opts.ToolboxOpts(),
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="line"),
            # title_opts=opts.TitleOpts(title="前5国家每年发文量")
        )
            .render(save_root + "43-前5国家每年发文量（河流图）.html")
    )


# 43-前5发文国家每年发文量（折线图）
def top_5_country_line():
    x_data = [str(i) for i in range(2009, 2021)]
    y_data_1 = [94, 94, 95, 87, 105, 102, 103, 95, 118, 127, 121, 74]   # USA
    y_data_2 = [50, 31, 72, 49, 76, 71, 82, 120, 116, 158, 184, 137]    # China
    y_data_3 = [34, 44, 48, 41, 57, 51, 36, 49, 40, 31, 29, 26]    # France
    y_data_4 = [21, 41, 27, 29, 18, 25, 26, 36, 23, 33, 22, 27]    # Australia
    y_data_5 = [22, 22, 32, 25, 23, 29, 26, 24, 28, 23, 23, 16]    # Canada


    c = (
        Line(init_opts=opts.InitOpts(width="1000px", height="500px", page_title="发文量前5期刊的每年发文量"))
            .set_global_opts(
            toolbox_opts=opts.ToolboxOpts(),
            tooltip_opts=opts.TooltipOpts(is_show=False),
            title_opts=opts.TitleOpts(title="发文量前5国家的每年发文量", pos_left="45%"),
            xaxis_opts=opts.AxisOpts(type_="category", name="Year",
                                     name_textstyle_opts=opts.TextStyleOpts(font_size=15),
                                     axistick_opts=opts.AxisTickOpts(is_align_with_label=True)),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
                name="发文量"
            ),
            legend_opts=opts.LegendOpts( pos_top="95%")
        )
            .add_xaxis(xaxis_data=x_data)
            .add_yaxis(
            series_name="USA",
            y_axis=y_data_1,
            symbol="circle",
            symbol_size=5,
            linestyle_opts = opts.LineStyleOpts(width=5, opacity=0.6),
            label_opts=opts.LabelOpts(is_show=False),
            markpoint_opts=opts.MarkPointOpts(
                data=[
                    opts.MarkPointItem(type_="max", name="最大值"),
                ],
            ),
        )
            .add_yaxis(
            series_name="China",
            y_axis=y_data_2,
            symbol="circle",
            symbol_size=5,
            linestyle_opts = opts.LineStyleOpts(width=5, opacity=0.6),
            label_opts=opts.LabelOpts(is_show=False),
            markpoint_opts=opts.MarkPointOpts(
                data=[
                    opts.MarkPointItem(type_="max", name="最大值"),
                ],
            ),
        )
            .add_yaxis(
            series_name="France",
            y_axis=y_data_3,
            symbol="circle",
            symbol_size=5,
            linestyle_opts = opts.LineStyleOpts(width=5, opacity=0.6),
            label_opts=opts.LabelOpts(is_show=False),
            markpoint_opts=opts.MarkPointOpts(
                data=[
                    opts.MarkPointItem(type_="max", name="最大值"),
                ],
            ),
        )
            .add_yaxis(
            series_name="Australia",
            y_axis=y_data_4,
            symbol="circle",
            symbol_size=5,
            linestyle_opts = opts.LineStyleOpts(width=5, opacity=0.6),
            label_opts=opts.LabelOpts(is_show=False),
            markpoint_opts=opts.MarkPointOpts(
                data=[
                    opts.MarkPointItem(type_="max", name="最大值"),
                ],
            ),
        )
            .add_yaxis(
            series_name="Canada",
            y_axis=y_data_5,
            symbol="circle",
            symbol_size=5,
            linestyle_opts = opts.LineStyleOpts(width=5, opacity=0.6),
            label_opts=opts.LabelOpts(is_show=False),
            markpoint_opts=opts.MarkPointOpts(
                data=[
                    opts.MarkPointItem(type_="max", name="最大值"),
                ],
            ),
        )
            .render(save_root + "43-前5国家每年发文量（多条折线图）.html")
    )


# 44-发文量前5国家独自发文与合作发文情况（堆叠柱状图）
def top5_country_by_oneself():
    x_data = ["USA", "China", "France", "Australia", "Canada"]
    y_data1 = [808, 714, 196, 158, 144]  # 前5国家独自发文量
    y_data2 = [407, 432, 290, 170, 149]  # 与其他国家合作发文量

    c = (
        Bar(init_opts=opts.InitOpts(width="600px", height="400px", bg_color="white"))
            .add_xaxis(x_data)
            .add_yaxis("alone", y_data1, stack="stack1", bar_width='60%')
            .add_yaxis("cooperation", y_data2, stack="stack1", bar_width='60%')
            .set_series_opts(label_opts=opts.LabelOpts(is_show=True, position="right"))
            .set_global_opts(
                toolbox_opts=opts.ToolboxOpts(),
                # title_opts=opts.TitleOpts(title="发文量前5国家独自发文与合作发文情况", pos_left="35%"),
                legend_opts=opts.LegendOpts(pos_bottom="2%")
        )
            .render(save_root + "44-发文量前5国家独自发文与合作发文情况（堆叠柱状图）.html")
    )


# 51-发文量前15机构的发文量（柱状图）
def top_15_org():
    x_data = ["USA ARS", "INRA", "Chinese Acad Sci", "China Agr Univ", "Chinese Acad Agr Sci",
              "Agr & Agri Food Canada", "Samuel Roberts Noble Fdn Inc", "CNRS", "Lanzhou Univ", "CSIC"]\
              # , "Nanjing Agr Univ", "Univ Minnesota", "Univ Toulouse", "Univ Wisconsin", "Univ Calif Davis",
              # "Northwest A&F Univ"]
        # , "Utah State Univ", "Ctr Biotechnol Borj Cedria", "Univ Western Australia",
        #       "King Saud Univ", "Isfahan Univ Technol"]
    y_data = [240, 227, 211, 167, 166, 160, 146, 130, 128, 114]  #, 109, 100, 89, 85, 70, 64]  #, 63, 56, 56, 45, 45]
    grid = Grid(init_opts=opts.InitOpts(bg_color="white"))
    c = (
        Bar(init_opts=opts.InitOpts(width="1600px", height="800px"))
            .add_xaxis(x_data)
            .add_yaxis("Number", y_data, bar_width='60%', color="#c23531", itemstyle_opts=opts.ItemStyleOpts(opacity=0.8))   # , itemstyle_opts=opts.ItemStyleOpts(opacity=0.8))
            .set_global_opts(
            toolbox_opts=opts.ToolboxOpts(),
            # title_opts=opts.TitleOpts(title="前15机构发文量", pos_left='50%'),
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(position="left", rotate=30, font_size=8),
                                     axistick_opts=opts.AxisTickOpts(is_align_with_label=True)),
            yaxis_opts=opts.AxisOpts(max_=250),
            legend_opts=opts.LegendOpts(pos_left="80%", pos_top="10%")
        )
    )
    grid.add(c, grid_opts=opts.GridOpts(pos_bottom="20%", pos_left='20%'))
    grid.render(save_root + "51-发文量前15机构的发文量（柱状图）.html")


# 52-发文前10机构每年发文量（河流图）
def top_10_org_river():
    x_data = ["USA ARS", "INRA", "Chinese Acad Sci", "China Agr Univ", "Chinese Acad Agr Sci",
              "Agr & Agri Food Canada", "Samuel Roberts Noble Fdn Inc", "CNRS", "Lanzhou Univ", "CSIC"]
    y_data = [
        # USA ARS
        ["2009", 23, "USA ARS"], ["2010", 19, "USA ARS"], ["2011", 17, "USA ARS"], ["2012", 14, "USA ARS"],
        ["2013", 24, "USA ARS"], ["2014", 17, "USA ARS"], ["2015", 22, "USA ARS"], ["2016", 13, "USA ARS"],
        ["2017", 32, "USA ARS"], ["2018", 23, "USA ARS"], ["2019", 18, "USA ARS"], ["2020", 18, "USA ARS"],
        # INRA
        ["2009", 17, "INRA"], ["2010", 26, "INRA"], ["2011", 21, "INRA"], ["2012", 20, "INRA"],
        ["2013", 33, "INRA"], ["2014", 32, "INRA"], ["2015", 19, "INRA"], ["2016", 26, "INRA"],
        ["2017", 12, "INRA"], ["2018", 10, "INRA"], ["2019", 8, "INRA"], ["2020", 3, "INRA"],
        # Chinese Acad Sci
        ["2009", 8, "Chinese Acad Sci"], ["2010", 10, "Chinese Acad Sci"], ["2011", 16, "Chinese Acad Sci"], ["2012", 8, "Chinese Acad Sci"],
        ["2013", 11, "Chinese Acad Sci"], ["2014", 15, "Chinese Acad Sci"], ["2015", 15, "Chinese Acad Sci"], ["2016", 25, "Chinese Acad Sci"],
        ["2017", 22, "Chinese Acad Sci"], ["2018", 24, "Chinese Acad Sci"], ["2019", 29, "Chinese Acad Sci"], ["2020", 28, "Chinese Acad Sci"],
        # China Agr Univ
        ["2009", 14, "China Agr Univ"], ["2010", 9, "China Agr Univ"], ["2011", 8, "China Agr Univ"], ["2012", 12, "China Agr Univ"],
        ["2013", 8, "China Agr Univ"], ["2014", 7, "China Agr Univ"], ["2015", 10, "China Agr Univ"], ["2016", 14, "China Agr Univ"],
        ["2017", 22, "China Agr Univ"], ["2018", 26, "China Agr Univ"], ["2019", 19, "China Agr Univ"], ["2020", 18, "China Agr Univ"],
        # Chinese Acad Agr Sci
        ["2009", 4, "Chinese Acad Agr Sci"], ["2010", 7, "Chinese Acad Agr Sci"], ["2011", 8, "Chinese Acad Agr Sci"], ["2012", 8, "Chinese Acad Agr Sci"],
        ["2013", 12, "Chinese Acad Agr Sci"], ["2014", 13, "Chinese Acad Agr Sci"], ["2015", 17, "Chinese Acad Agr Sci"], ["2016", 16, "Chinese Acad Agr Sci"],
        ["2017", 16, "Chinese Acad Agr Sci"], ["2018", 21, "Chinese Acad Agr Sci"], ["2019", 31, "Chinese Acad Agr Sci"], ["2020", 13, "Chinese Acad Agr Sci"],
        # Agr & Agri Food Canada
        ["2009", 11, "Agr & Agri Food Canada"], ["2010", 13, "Agr & Agri Food Canada"], ["2011", 15, "Agr & Agri Food Canada"], ["2012", 13, "Agr & Agri Food Canada"],
        ["2013", 13, "Agr & Agri Food Canada"], ["2014", 16, "Agr & Agri Food Canada"], ["2015", 14, "Agr & Agri Food Canada"], ["2016", 10, "Agr & Agri Food Canada"],
        ["2017", 13, "Agr & Agri Food Canada"], ["2018", 14, "Agr & Agri Food Canada"], ["2019", 18, "Agr & Agri Food Canada"], ["2020", 10, "Agr & Agri Food Canada"],
        # Samuel Roberts Noble Fdn Inc
        ["2009", 13, "Samuel Roberts Noble Fdn Inc"], ["2010", 9, "Samuel Roberts Noble Fdn Inc"], ["2011", 23, "Samuel Roberts Noble Fdn Inc"], ["2012", 17, "Samuel Roberts Noble Fdn Inc"],
        ["2013", 18, "Samuel Roberts Noble Fdn Inc"], ["2014", 21, "Samuel Roberts Noble Fdn Inc"], ["2015", 17, "Samuel Roberts Noble Fdn Inc"], ["2016", 13, "Samuel Roberts Noble Fdn Inc"],
        ["2017", 6, "Samuel Roberts Noble Fdn Inc"], ["2018", 5, "Samuel Roberts Noble Fdn Inc"], ["2019", 3, "Samuel Roberts Noble Fdn Inc"], ["2020", 1, "Samuel Roberts Noble Fdn Inc"],
        # CNRS
        ["2009", 15, "CNRS"], ["2010", 8, "CNRS"], ["2011", 13, "CNRS"], ["2012", 19, "CNRS"],
        ["2013", 23, "CNRS"], ["2014", 21, "CNRS"], ["2015", 15, "CNRS"], ["2016", 11, "CNRS"],
        ["2017", 2, "CNRS"], ["2018", 1, "CNRS"], ["2019", 2, "CNRS"], ["2020", 0, "CNRS"],
        # Lanzhou Univ
        ["2009", 7, "Lanzhou Univ"], ["2010", 0, "Lanzhou Univ"], ["2011", 13, "Lanzhou Univ"], ["2012", 4, "Lanzhou Univ"],
        ["2013", 9, "Lanzhou Univ"], ["2014", 7, "Lanzhou Univ"], ["2015", 13, "Lanzhou Univ"], ["2016", 11, "Lanzhou Univ"],
        ["2017", 8, "Lanzhou Univ"], ["2018", 17, "Lanzhou Univ"], ["2019", 21, "Lanzhou Univ"], ["2020", 18, "Lanzhou Univ"],
        # CSIC
        ["2009", 13, "CSIC"], ["2010", 12, "CSIC"], ["2011", 7, "CSIC"], ["2012", 7, "CSIC"],
        ["2013", 11, "CSIC"], ["2014", 17, "CSIC"], ["2015", 11, "CSIC"], ["2016", 7, "CSIC"],
        ["2017", 7, "CSIC"], ["2018", 8, "CSIC"], ["2019", 8, "CSIC"], ["2020", 6, "CSIC"],
    ]


    # 河流图
    c = (
        ThemeRiver(init_opts=opts.InitOpts(width="800px", height="600px", bg_color="white"))
            .add(
            series_name=x_data,
            data=y_data,
            singleaxis_opts=opts.SingleAxisOpts(
                pos_top="50", pos_bottom="50", type_="value", min_="2009", max_="2020"
            ),
            label_opts=opts.LabelOpts(font_size=15, position="insideLeft", distance=10, font_style="oblique")
        )
            .set_global_opts(
            toolbox_opts=opts.ToolboxOpts(),
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="line"),
            # title_opts=opts.TitleOpts(title="前10机构每年发文量")
        )
            .render(save_root + "52-发文前10机构每年发文量（河流图）.html")
    )


# 52-前5发文机构每年发文量（折线图）
def top_5_org_line():
    x_data = [str(i) for i in range(2009, 2021)]
    y_data_1 = [23, 19, 17, 14, 24, 17, 22, 13, 32, 23, 18, 18]   # USA ARS
    y_data_2 = [17, 26, 21, 20, 33, 32, 19, 26, 12, 10, 8, 3]    # INRA
    y_data_3 = [8, 10, 16, 8, 11, 15, 15, 25, 22, 24, 29, 28]    # Chinese Acad Sci
    y_data_4 = [14, 9, 8, 12, 8, 7, 10, 14, 22, 26, 19, 18]    # China Agr Univ
    y_data_5 = [4, 7, 8, 8, 12, 13, 17, 16, 16, 21, 31, 13]    # Chinese Acad Agr Sci
    y_data_6 = [11, 13, 15, 13, 13, 16, 14, 10, 13, 14, 18, 10]   # Agr & Agri Food Canada
    y_data_7 = [13, 9, 23, 17, 18, 21, 17, 13, 6, 5, 3, 1]    # Samuel Roberts Noble Fdn Inc
    y_data_8 = [15, 8, 13, 19, 23, 21, 15, 11, 2, 1, 2, 0]    # CNRS
    y_data_9 = [7, 0, 13, 4, 9, 7, 13, 11, 8, 17, 21, 18]    # Lanzhou Univ
    y_data_10 = [13, 12, 7, 7, 11, 17, 11, 7, 7, 8, 8, 6]    # CSIC


    c = (
        Line(init_opts=opts.InitOpts(width="1000px", height="500px"))
            .set_global_opts(
            toolbox_opts=opts.ToolboxOpts(),
            tooltip_opts=opts.TooltipOpts(is_show=False),
            title_opts=opts.TitleOpts(title="发文量前5机构的每年发文量", pos_left="45%"),
            xaxis_opts=opts.AxisOpts(type_="category", name="Year",
                                     name_textstyle_opts=opts.TextStyleOpts(font_size=15),
                                     axistick_opts=opts.AxisTickOpts(is_align_with_label=True)),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
                name="发文量"
            ),
            legend_opts=opts.LegendOpts( pos_top="95%")
        )
            .add_xaxis(xaxis_data=x_data)
            .add_yaxis(
            series_name="USA ARS",
            y_axis=y_data_1,
            symbol="circle",
            symbol_size=5,
            linestyle_opts = opts.LineStyleOpts(width=5, opacity=0.6),
            label_opts=opts.LabelOpts(is_show=False),
            markpoint_opts=opts.MarkPointOpts(
                data=[
                    opts.MarkPointItem(type_="max", name="最大值"),
                ],
            ),
        )
            .add_yaxis(
            series_name="INRA",
            y_axis=y_data_2,
            symbol="circle",
            symbol_size=5,
            linestyle_opts = opts.LineStyleOpts(width=5, opacity=0.6),
            label_opts=opts.LabelOpts(is_show=False),
            markpoint_opts=opts.MarkPointOpts(
                data=[
                    opts.MarkPointItem(type_="max", name="最大值"),
                ],
            ),
        )
            .add_yaxis(
            series_name="Chinese Acad Sci",
            y_axis=y_data_3,
            symbol="circle",
            symbol_size=5,
            linestyle_opts = opts.LineStyleOpts(width=5, opacity=0.6),
            label_opts=opts.LabelOpts(is_show=False),
            markpoint_opts=opts.MarkPointOpts(
                data=[
                    opts.MarkPointItem(type_="max", name="最大值"),
                ],
            ),
        )
            .add_yaxis(
            series_name="China Agr Univ",
            y_axis=y_data_4,
            symbol="circle",
            symbol_size=5,
            linestyle_opts = opts.LineStyleOpts(width=5, opacity=0.6),
            label_opts=opts.LabelOpts(is_show=False),
            markpoint_opts=opts.MarkPointOpts(
                data=[
                    opts.MarkPointItem(type_="max", name="最大值"),
                ],
            ),
        )
            .add_yaxis(
            series_name="Chinese Acad Agr Sci",
            y_axis=y_data_5,
            symbol="circle",
            symbol_size=5,
            linestyle_opts = opts.LineStyleOpts(width=5, opacity=0.6),
            label_opts=opts.LabelOpts(is_show=False),
            markpoint_opts=opts.MarkPointOpts(
                data=[
                    opts.MarkPointItem(type_="max", name="最大值"),
                ],
            ),
        )
        #     .add_yaxis(
        #     series_name="Agr & Agri Food Canada",
        #     y_axis=y_data_6,
        #     symbol="circle",
        #     symbol_size=5,
        #     linestyle_opts = opts.LineStyleOpts(width=5, opacity=0.6),
        #     label_opts=opts.LabelOpts(is_show=False),
        #     markpoint_opts=opts.MarkPointOpts(
        #         data=[
        #             opts.MarkPointItem(type_="max", name="最大值"),
        #         ],
        #     ),
        # )
        #     .add_yaxis(
        #     series_name="Samuel Roberts Noble Fdn Inc",
        #     y_axis=y_data_7,
        #     symbol="circle",
        #     symbol_size=5,
        #     linestyle_opts = opts.LineStyleOpts(width=5, opacity=0.6),
        #     label_opts=opts.LabelOpts(is_show=False),
        #     markpoint_opts=opts.MarkPointOpts(
        #         data=[
        #             opts.MarkPointItem(type_="max", name="最大值"),
        #         ],
        #     ),
        # )
        #     .add_yaxis(
        #     series_name="CNRS",
        #     y_axis=y_data_8,
        #     symbol="circle",
        #     symbol_size=5,
        #     linestyle_opts = opts.LineStyleOpts(width=5, opacity=0.6),
        #     label_opts=opts.LabelOpts(is_show=False),
        #     markpoint_opts=opts.MarkPointOpts(
        #         data=[
        #             opts.MarkPointItem(type_="max", name="最大值"),
        #         ],
        #     ),
        # )
        #     .add_yaxis(
        #     series_name="Lanzhou Univ",
        #     y_axis=y_data_9,
        #     symbol="circle",
        #     symbol_size=5,
        #     linestyle_opts = opts.LineStyleOpts(width=5, opacity=0.6),
        #     label_opts=opts.LabelOpts(is_show=False),
        #     markpoint_opts=opts.MarkPointOpts(
        #         data=[
        #             opts.MarkPointItem(type_="max", name="最大值"),
        #         ],
        #     ),
        # )
        #     .add_yaxis(
        #     series_name="CSIC",
        #     y_axis=y_data_10,
        #     symbol="circle",
        #     symbol_size=5,
        #     linestyle_opts = opts.LineStyleOpts(width=5, opacity=0.6),
        #     label_opts=opts.LabelOpts(is_show=False),
        #     markpoint_opts=opts.MarkPointOpts(
        #         data=[
        #             opts.MarkPointItem(type_="max", name="最大值"),
        #         ],
        #     ),
        # )
            .render(save_root + "52-前5发文机构每年发文量（多条折线图）.html")
    )


# 61-资金来源前十（柱状图）
def top_10_financial_bar():
    # 合并欧盟之后
    x_data = ["National Natural Science Foundation of China", "National Science Foundation (NSF)", "European Union(EU)",
              "United States Department of Agriculture(USDA)", "National Basic Research Program of China(973 program)"]\
        # ,
        #       "Fundamental Research Funds for the Central Universities", "Chinese Academy of Sciences",
        #       "National Key R&D Program of China", "Samuel Roberts Noble Foundation", "China Agriculture Research System"]
    y_data = [631, 237, 167, 166, 145]  #, 91, 82, 75, 72, 68]

    grid = Grid()
    c = (
        Bar(init_opts=opts.InitOpts(width="1000px", height="500px"))
            .add_xaxis(x_data)
            .add_yaxis("Number", y_data, bar_width='60%', itemstyle_opts=opts.ItemStyleOpts(opacity=0.8))
            .set_global_opts(
            # toolbox_opts=opts.ToolboxOpts(),
            # title_opts=opts.TitleOpts(title="资金来源前十", pos_left='50%'),
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(position="left", rotate=20, font_size=10),
                                     axistick_opts=opts.AxisTickOpts(is_align_with_label=True)),
            yaxis_opts=opts.AxisOpts(max_=650),
            legend_opts=opts.LegendOpts(pos_left="80%", pos_top="10%")
            # datazoom_opts=opts.DataZoomOpts(pos_bottom='2%'),
        )
        # .render(save_root + "2-前十期刊发文量.html")
    )
    grid.add(c, grid_opts=opts.GridOpts(pos_bottom="40%", pos_left='20%'))
    grid.render(save_root + "61-资金来源前十+eu（柱状图）.html")


# 61-资金来源前5（横着的柱状图）
def top_10_financial_bar_horizontal():
    # 合并欧盟之后
    x_data = ["National Natural Science Foundation of China", "National Science Foundation (NSF)", "European Union(EU)",
              "United States Department of Agriculture(USDA)", "National Basic Research Program of China(973 program)"] \
        # ,
    #       "Fundamental Research Funds for the Central Universities", "Chinese Academy of Sciences",
    #       "National Key R&D Program of China", "Samuel Roberts Noble Foundation", "China Agriculture Research System"]
    y_data = [631, 237, 167, 166, 145]  #, 91, 82, 75, 72, 68]

    grid = Grid(init_opts=opts.InitOpts(bg_color="white"))
    c = (
        Bar(init_opts=opts.InitOpts(width="1000px", height="500px"))
            .add_xaxis(x_data)
            .add_yaxis("Number", y_data, bar_width='60%', itemstyle_opts=opts.ItemStyleOpts(opacity=0.8))
            .reversal_axis()
            .set_series_opts(label_opts=opts.LabelOpts(position="right"))
            .set_global_opts(
            toolbox_opts=opts.ToolboxOpts(),
            # title_opts=opts.TitleOpts(title="资金来源前十", pos_left='50%'),
            # xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(position="left", rotate=20, font_size=10),
            #                          axistick_opts=opts.AxisTickOpts(is_align_with_label=True)),
            # yaxis_opts=opts.AxisOpts(max_=650),
            legend_opts=opts.LegendOpts(pos_left="80%", pos_top="10%")
            # datazoom_opts=opts.DataZoomOpts(pos_bottom='2%'),
        )
        # .render(save_root + "2-前十期刊发文量.html")
    )
    grid.add(c, grid_opts=opts.GridOpts(pos_bottom="20%", pos_left='40%'))
    grid.render(save_root + "61-资金来源前5_horizontal（柱状图）.html")



# 62-资金前5每年资助论文数量（折线图）
def top_5_financial_time_line():
    x_data = [str(i) for i in range(2009, 2021)]
    y_data_1 = [16, 8, 29, 20, 40, 42, 44, 67, 67, 95, 108, 95]   # National Natural Science Foundation of China
    y_data_2 = [18, 18, 21, 16, 21, 23, 19, 16, 19, 25, 22, 19]    # National Science Foundation (NSF)
    y_data_3 = [17, 13, 17, 6, 9, 16, 23, 11, 16, 8, 20, 11]      # European Union(EU)
    y_data_4 = [14, 12, 18, 11, 10, 11, 17, 7, 18, 18, 20, 10]    # United States Department of Agriculture(USDA)
    y_data_5 = [12, 5, 19, 6, 16, 12, 14, 25, 8, 12, 10, 6]    # National Basic Research Program of China(973 program)



    c = (
        Line(init_opts=opts.InitOpts(width="1000px", height="500px", page_title="资金前5每年资助论文数量", bg_color="white"))
            .set_global_opts(
            toolbox_opts=opts.ToolboxOpts(),
            # tooltip_opts=opts.TooltipOpts(is_show=False),
            # title_opts=opts.TitleOpts(title="资金前5每年资助论文数量", pos_left="45%"),
            xaxis_opts=opts.AxisOpts(type_="category",
                                     name_textstyle_opts=opts.TextStyleOpts(font_size=15),
                                     axistick_opts=opts.AxisTickOpts(is_align_with_label=True)),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
            ),
            legend_opts=opts.LegendOpts(pos_left="12%", pos_top="15%", orient="vertical")
        )
            .add_xaxis(xaxis_data=x_data)
            .add_yaxis(
            series_name="National Natural Science Foundation of China",
            y_axis=y_data_1,
            symbol="circle",
            symbol_size=5,
            linestyle_opts = opts.LineStyleOpts(width=5, opacity=0.6),
            label_opts=opts.LabelOpts(is_show=False),
            markpoint_opts=opts.MarkPointOpts(
                data=[
                    opts.MarkPointItem(type_="max", name="最大值"),
                ],
            ),
        )
            .add_yaxis(
            series_name="National Science Foundation (NSF)",
            y_axis=y_data_2,
            symbol="circle",
            symbol_size=5,
            linestyle_opts = opts.LineStyleOpts(width=5, opacity=0.6),
            label_opts=opts.LabelOpts(is_show=False),
            markpoint_opts=opts.MarkPointOpts(
                data=[
                    opts.MarkPointItem(type_="max", name="最大值"),
                ],
            ),
        )
            .add_yaxis(
            series_name="European Union(EU)",
            y_axis=y_data_3,
            symbol="circle",
            symbol_size=5,
            linestyle_opts = opts.LineStyleOpts(width=5, opacity=0.6),
            label_opts=opts.LabelOpts(is_show=False),
            markpoint_opts=opts.MarkPointOpts(
                data=[
                    opts.MarkPointItem(type_="max", name="最大值"),
                ],
            ),
        )
            .add_yaxis(
            series_name="United States Department of Agriculture(USDA)",
            y_axis=y_data_4,
            symbol="circle",
            symbol_size=5,
            linestyle_opts = opts.LineStyleOpts(width=5, opacity=0.6),
            label_opts=opts.LabelOpts(is_show=False),
            markpoint_opts=opts.MarkPointOpts(
                data=[
                    opts.MarkPointItem(type_="max", name="最大值"),
                ],
            ),
        )
            .add_yaxis(
            series_name="National Basic Research Program of China(973 program)",
            y_axis=y_data_5,
            symbol="circle",
            symbol_size=5,
            linestyle_opts = opts.LineStyleOpts(width=5, opacity=0.6),
            label_opts=opts.LabelOpts(is_show=False),
            markpoint_opts=opts.MarkPointOpts(
                data=[
                    opts.MarkPointItem(type_="max", name="最大值"),
                ],
            ),
        )
            .render(save_root + "62-资金前5每年资助论文数量（折线图）.html")
    )


# 71-前10学科分布，柱状图
def top_10_subject_scatter():
    x_data = ["Plant Sciences", "Agronomy", "Agriculture, Dairy & Animal Science", "Environmental Sciences",
              "Agriculture, Multidisciplinary", "Biotechnology & Applied Microbiology",
              "Biochemistry & Molecular Biology", "Food Science & Technology", "Genetics & Heredity", "Soil Science"]
    y_data = [1542, 804, 562, 387, 386, 371, 370, 280, 225, 222]

    grid = Grid(init_opts=opts.InitOpts(bg_color="white"))
    c = (
        Bar(init_opts=opts.InitOpts(width=" 800px", height="600px"))
            .add_xaxis(x_data)
            .add_yaxis("Number", y_data, bar_width='60%', itemstyle_opts=opts.ItemStyleOpts(opacity=0.8))
            .reversal_axis()
            .set_series_opts(label_opts=opts.LabelOpts(position="right"))
            .set_global_opts(
            # title_opts=opts.TitleOpts(title="学科排名前十", pos_left='50%'),
            # xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(position="left", rotate=30, font_size=10),
            #                          axistick_opts=opts.AxisTickOpts(is_align_with_label=True)),
            # yaxis_opts=opts.AxisOpts(max_=1600),
            legend_opts=opts.LegendOpts(pos_left="80%", pos_top="10%"),
            toolbox_opts=opts.ToolboxOpts(),
        )
    )
    grid.add(c, grid_opts=opts.GridOpts(pos_bottom="10%", pos_left='30%'))
    grid.render(save_root + "71-前10学科分布.html")


# 72-前十国家的学科分布，雷达图
def top_10_country_subject():
    v1 = [[210, 154, 47, 58, 64]]  # Agronomy
    v2 = [[125, 103, 49, 39, 58]]     # Agriculture, Dairy & Animal Science
    v3 = [[53, 135, 18, 16, 19]]     # Environmental Sciences
    v4 = [[42, 89, 11, 62, 14]]     # Agriculture, Multidisciplinary
    v5 = [[101, 90, 36, 8, 20]]     # Biotechnology & Applied Microbiology

    (
        Radar(init_opts=opts.InitOpts(width="1280px", height="720px"))
            .add_schema(
            schema=[
                opts.RadarIndicatorItem(name="USA", max_=827),
                opts.RadarIndicatorItem(name="China", max_=780),
                opts.RadarIndicatorItem(name="France", max_=226),
                opts.RadarIndicatorItem(name="Australia", max_=214),
                opts.RadarIndicatorItem(name="Canada", max_=212),
            ],
            splitarea_opt=opts.SplitAreaOpts(
                is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
            ),
            textstyle_opts=opts.TextStyleOpts(color="black"),
        )
            .add(
            series_name="Agronomy",
            data=v1,
            linestyle_opts=opts.LineStyleOpts(color="#c23531", width=3, opacity=0.8),
        )
            .add(
            series_name="Agriculture, Dairy & Animal Science",
            data=v2,
            linestyle_opts=opts.LineStyleOpts(color="#2f4554", width=3, opacity=0.8),
        )
            .add(
            series_name="Environmental Sciences",
            data=v3,
            linestyle_opts=opts.LineStyleOpts(color="#61a0a8", width=3, opacity=0.8),
        )
            .add(
            series_name="Agriculture, Multidisciplinary",
            data=v4,
            linestyle_opts=opts.LineStyleOpts(color="#d48265", width=3, opacity=0.8),
        )
            .add(
            series_name="Biotechnology & Applied Microbiology",
            data=v5,
            linestyle_opts=opts.LineStyleOpts(color="#91c7ae", width=3, opacity=0.8),
        )
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(
            # title_opts=opts.TitleOpts(title="前5国家中前10学科的分布情况"),
            legend_opts=opts.LegendOpts(orient="vertical", pos_top="50%", pos_left="5%"),
            toolbox_opts=opts.ToolboxOpts(),
        )
            .render(save_root + "72-前5国家中前10学科的分布情况.html")
    )

# 72-Plant Sciences在前10国家中的占比情况
def Plant_Sciences():
    v1 = [[388, 366, 260, 114, 81, 124, 61, 94, 83, 40]]

    c = (
        Radar()
            .add_schema(
            schema=[
                opts.RadarIndicatorItem(name="USA", max_=1215),
                opts.RadarIndicatorItem(name="China", max_=1146),
                opts.RadarIndicatorItem(name="France", max_=486),
                opts.RadarIndicatorItem(name="Australia", max_=328),
                opts.RadarIndicatorItem(name="Canada", max_=293),
                opts.RadarIndicatorItem(name="Spain", max_=290),
                opts.RadarIndicatorItem(name="Iran", max_=256),
                opts.RadarIndicatorItem(name="Italy", max_=218),
                opts.RadarIndicatorItem(name="Germany", max_=186),
                opts.RadarIndicatorItem(name="Poland", max_=143),
            ],
            textstyle_opts=opts.TextStyleOpts(font_size=15,color="black"),
            axisline_opt=opts.AxisLineOpts()
        )
            .add("Plant Sciences", v1)
            .set_series_opts(label_opts=opts.LabelOpts(is_show=True))
            .set_global_opts(
            legend_opts=opts.LegendOpts(pos_left="5%", pos_top="50%"),
            title_opts=opts.TitleOpts(title="Plant Sciences在前10国家中的占比情况", pos_left="30%"),
            toolbox_opts=opts.ToolboxOpts(),
        )
            .render(save_root + "72-Plant Sciences在前10国家中的占比情况.html")
    )

# 73-交叉学科（热力图）
def interdisciplinary():
    import second.subject as subject
    subject_list, value = subject.main()

    grid = Grid(init_opts=opts.InitOpts(width="1200px", height="800px", bg_color="white"))
    c = (
        HeatMap(init_opts=opts.InitOpts(width="800px", height="600px"))
            .add_xaxis(subject_list)
            .add_yaxis(
            "Co occurrence frequency",
            subject_list,
            value,
            label_opts=opts.LabelOpts(is_show=False, position="inside"),
        )
            .set_global_opts(
            # title_opts=opts.TitleOpts(title="学科共现频次"),
            visualmap_opts=opts.VisualMapOpts(pos_left="92%", max_=100, pos_bottom="20%", range_color=['#D7DA8B', '#E15457']),
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=30, font_size=10)),
            legend_opts=opts.LegendOpts(pos_top="2%"),
            toolbox_opts=opts.ToolboxOpts(),
        )
            # .render(save_root + "73-交叉学科（热力图）.html")
    )
    grid.add(c, grid_opts=opts.GridOpts(pos_bottom="20%", pos_left='22%'))
    grid.render(save_root + "73-交叉学科（热力图）2.html")

# 8-战略坐标（不能运行，只包含js代码）
def strategic_coordinates():
    #     // 散点数据
    # let marksData = [
    #     {
    #         name: 'ID1:Bioremediation',
    #         value: [1430000, 416.56315789473683],
    #         symbolSize: 48.6,
    #     },
    #     {
    #         name: 'ID2:Mechanism of mycorrhizal symbiosis',
    #         value: [888012, 544.8736842105263],
    #         symbolSize: 69.0,
    #     },
    #     {
    #         name: 'ID3:Field production1',
    #         value: [1392107, 426.36842105263156],
    #         symbolSize: 29.5,
    #     },
    #     {
    #         name: 'ID4:Insect ecology',
    #         value: [1094511, 195.2736842105263],
    #         symbolSize: 41.7,
    #     },
    #     {
    #         name: 'ID5:Feeding value',
    #         value: [1195329, 467.8894736842105],
    #         symbolSize: 56.2,
    #     },
    #     {
    #         name: 'ID6:Seed treatment',
    #         value: [1133865, 284.7105263157895],
    #         symbolSize: 33.6,
    #     },
    #     {
    #         name: 'ID7:Bioactive ingredients',
    #         value: [1259940, 250.76315789473685],
    #         symbolSize: 43.3,
    #     },
    #     {
    #         name: 'ID8:Field production2',
    #         value: [1500806, 527.3631578947368],
    #         symbolSize: 61.5,
    #     },
    #     {
    #         name: 'ID9:Resistance to abiotic stress',
    #         value: [1409970, 464.93157894736845],
    #         symbolSize: 54.9,
    #     },
    #     {
    #         name: 'ID10:Protein genomics',
    #         value: [1340000, 450.3526315789474],
    #         symbolSize: 62.8,
    #     },
    # ]
    # // 中心线
    # centerLine = [
    #     {
    #         name: 'Density', xAxis: 1266511.2
    #     },
    #     {
    #         name: 'Center', yAxis: 401.8
    #     }
    # ]
    # // 中心点
    # centerMark = [
    #     {
    #         coord: [1266511.2, 401.8]
    #     }
    # ]
    #
    # option = {
    #              toolbox: {
    #                  show: true,
    #                  feature: {
    #                      saveAsImage: {}
    #                  }
    #              },
    #          //title: {
    #                   //    text: '主题战略坐标',
    # //},
    # tooltip: {
    #     axisPointer: {
    #         show: true,
    #         type: 'cross',
    #         lineStyle: {
    #             type: 'dashed',
    #             width: 2
    #         },
    #         label: {
    #             backgroundColor: '#555'
    #         }
    #     }
    # },
    # grid: {
    #     left: 50,
    #     right: 50,
    #     bottom: '4%',
    #     top: '6%',
    #     containLabel: true
    # },
    # xAxis: {
    #     show: false,
    #     scale: true,
    #     max: 1750000,
    #     min: 750000,
    #     axisLine: {
    #         lineStyle: {
    #             color: '#ddd'
    #         }
    #     },
    #     axisLabel: {
    #         color: '#666'
    #     },
    #     splitLine: {
    #         lineStyle: {
    #             color: '#eee'
    #         }
    #     }
    # },
    # yAxis: {
    #     show: false,
    #     scale: true,
    #     max: 650,
    #     min: 150,
    #     axisLine: {
    #         lineStyle: {
    #             color: '#ddd'
    #         }
    #     },
    #     axisLabel: {
    #         color: '#666'
    #     },
    #     splitLine: {
    #         lineStyle: {
    #             color: '#eee'
    #         }
    #     }
    # },
    # series: [{
    #     type: 'scatter',
    #     data: marksData,
    #     label: {
    #         show: true,
    #         position: 'bottom',
    #         formatter: '{b}'
    #     },
    #     itemStyle: {
    #         shadowBlur: 2,
    #         shadowColor: 'rgba(120, 36, 50, 1)',
    #         shadowOffsetY: 1,
    #         color: function (e) {
    #             let randomColor = 'rgba(' + Math.floor(Math.random() * 240) + ',' + Math.floor(Math.random() * 240) + ',' + Math.floor(Math.random() * 240) + ',' + '.8' + ')'
    # return randomColor.substring()
    # },
    # },
    # // 各象限区域
    # markArea: {
    #     silent: true,
    #     data: [
    # // 第一象限
    # [{
    #      name: '第一象限',
    #      xAxis: 40, // x 轴开始位置
    #  yAxis: 70, // y 轴结束位置(直接取最大值)
    # itemStyle: {
    #     color: 'rgba(56, 180, 139, .1)'
    # },
    # label: {
    #     position: 'inside',
    #     color: 'rgba(0, 0, 0, .1)',
    #     fontSize: 22
    # }
    # }, {
    #     yAxis: 40 // y轴开始位置
    # }],
    # // 第二象限
    # [{
    #      name: '第二象限',
    #      yAxis: 70, // y 轴结束位置(直接取最大值)
    #  itemStyle: {
    #     color: 'rgba(68, 97, 123, .1)'
    # },
    # label: {
    #     position: 'inside',
    #     color: 'rgba(0, 0, 0, .1)',
    #     fontSize: 22
    # }
    # }, {
    #        xAxis: 40, // x 轴结束位置
    # yAxis: 40 // y轴开始位置
    # }],
    # // 第三象限
    # [{
    #      name: '第三象限',
    #      yAxis: 40, // y 轴结束位置
    #  itemStyle: {
    #     color: 'rgba(191, 120, 58, .1)'
    # },
    # label: {
    #     position: 'inside',
    #     color: 'rgba(0, 0, 0, .1)',
    #     fontSize: 22
    # }
    # }, {
    #        xAxis: 40, // x 轴结束位置
    # yAxis: 10 // y轴开始位置
    # }],
    # // 第四象限
    # [{
    #      name: '第四象限',
    #      xAxis: 40, // x 轴开始位置
    #  yAxis: 40, // y 轴结束位置
    # itemStyle: {
    #     color: 'rgba(116, 83, 153, .1)'
    # },
    # label: {
    #     position: 'inside',
    #     color: 'rgba(0, 0, 0, .1)',
    #     fontSize: 22
    # }
    # }, {
    #     yAxis: 10 // y轴开始位置
    # }]
    # ]
    # },
    # // 中心点交集象限轴
    # markLine: {
    #               silent: true, // 是否不响应鼠标事件
    # precision: 2, // 精度
    # lineStyle: {
    # type: 'solid',
    # color: '#00aca6'
    # },
    # label: {
    # color: '#00aca6',
    # position: 'end',
    # formatter: '{b}'
    # },
    # data: centerLine
    # },
    # // 中心点
    # markPoint: {
    #     symbol: 'roundRect',
    #     symbolSize: 15,
    #     itemStyle: {
    # color: 'rgba(234, 85, 6, .8)'
    # },
    # label: {
    # position: 'top'
    # },
    # data: centerMark
    # }
    # }]
    # }
    pass

# 9-主题分布图
def topic_distribution():
    color_list = ['#c23531','#2f4554', '#61a0a8', '#d48265', '#91c7ae','#749f83',  '#ca8622', '#bda29a','#6e7074', "#8B658B"]

    # 两个主题之间的余弦相似度
    # all
    relevance_dict = {'0-1': 0.14597889763837907, '0-2': 0.21294138590488337, '0-3': 0.3313919986133031,
                      '0-4': 0.21855211736430682, '0-5': 0.2920327786376364, '0-6': 0.370822801865742,
                      '0-7': 0.5468410809624057, '0-8': 0.32323725014729016, '0-9': 0.10333013044207018,
                      '1-2': 0.08654094958071583, '1-3': 0.0872715830584672, '1-4': 0.04854818635530201,
                      '1-5': 0.05994768481316778, '1-6': 0.13127153786271323, '1-7': 0.05643123921175691,
                      '1-8': 0.228238363030859, '1-9': 0.46685083215264833, '2-3': 0.2802521918126509,
                      '2-4': 0.24654179305500734, '2-5': 0.16817141301127947, '2-6': 0.21354440281840584,
                      '2-7': 0.3843326586147106, '2-8': 0.1412008322765039, '2-9': 0.12424562442963971,
                      '3-4': 0.20549086432582275, '3-5': 0.3091346693311201, '3-6': 0.4235165168076697,
                      '3-7': 0.5081328511993011, '3-8': 0.2995790532401047, '3-9': 0.23679807820064033,
                      '4-5': 0.2922800531553708, '4-6': 0.29529890363927086, '4-7': 0.3632523350472002,
                      '4-8': 0.18901422156406908, '4-9': 0.07454676043133053, '5-6': 0.36638156095136876,
                      '5-7': 0.4529117371266725, '5-8': 0.2766980832834005, '5-9': 0.10292840559550302,
                      '6-7': 0.5368943775102464, '6-8': 0.414972028784464, '6-9': 0.21152473148119733,
                      '7-8': 0.4374291758902374, '7-9': 0.17796748762303916, '8-9': 0.27116089641721924}

    # 2009-2012
    # relevance_dict = {'0-1': 0.2981823757009591, '0-2': 0.23984612627918192, '0-3': 0.3258847821530329, '0-4': 0.13238798126912768, '0-5': 0.07533373396079798, '0-6': 0.20647032760136666, '0-7': 0.2553806608030987, '0-8': 0.27616044218567865, '0-9': 0.44163673521956837, '1-2': 0.38147155406837524, '1-3': 0.45643840460550783, '1-4': 0.2347955521652748, '1-5': 0.09919746848135666, '1-6': 0.05477500358678642, '1-7': 0.2998355006746772, '1-8': 0.5185707706850843, '1-9': 0.4090464088437175, '2-3': 0.3485171639287014, '2-4': 0.16153962407293587, '2-5': 0.11403096612048183, '2-6': 0.10174243475793258, '2-7': 0.230412950598882, '2-8': 0.32726159588645054, '2-9': 0.3004632041406711, '3-4': 0.40619696349360007, '3-5': 0.03069678712496744, '3-6': 0.08830335502607876, '3-7': 0.40448858692916023, '3-8': 0.4941851701800149, '3-9': 0.45356117669959406, '4-5': 0.0375959524963306, '4-6': 0.043706413938645584, '4-7': 0.3136953092153345, '4-8': 0.2672391224511457, '4-9': 0.1903195614488093, '5-6': 0.27624647573711997, '5-7': 0.04445167766241859, '5-8': 0.10935174578958021, '5-9': 0.029383198762531315, '6-7': 0.044444389671799214, '6-8': 0.03148226306375116, '6-9': 0.03783397047807209, '7-8': 0.3357001119343291, '7-9': 0.3003716490334713, '8-9': 0.3995827150714771}

    # 2013-2016
    # relevance_dict = {'0-1': 0.28387419952465043, '0-2': 0.43797913526083615, '0-3': 0.04537192794030386, '0-4': 0.3509503255011747, '0-5': 0.0866084717217657, '0-6': 0.2736960764976254, '0-7': 0.31094049002115526, '0-8': 0.370989941038437, '0-9': 0.2372396619586547, '1-2': 0.24623443501318776, '1-3': 0.040305979633050465, '1-4': 0.29270671291844474, '1-5': 0.03530799719666533, '1-6': 0.11081969517140482, '1-7': 0.13723388030682535, '1-8': 0.19912968212285495, '1-9': 0.15035570508109028, '2-3': 0.06623614156222825, '2-4': 0.4879414859165981, '2-5': 0.03815359365830067, '2-6': 0.36179350092499446, '2-7': 0.3253737725691623, '2-8': 0.38844490726706987, '2-9': 0.37390619969412026, '3-4': 0.09621609381105627, '3-5': 0.2443434089001318, '3-6': 0.319533787211172, '3-7': 0.054697713425387796, '3-8': 0.03437483705534485, '3-9': 0.15740712473691867, '4-5': 0.08956107246518216, '4-6': 0.27926715580935685, '4-7': 0.2997771252260069, '4-8': 0.3917565559411965, '4-9': 0.3596192140903021, '5-6': 0.12848112059478475, '5-7': 0.047567657478685944, '5-8': 0.1530177746494486, '5-9': 0.11338049272971173, '6-7': 0.4012391959009842, '6-8': 0.24061776089991987, '6-9': 0.2474309786605821, '7-8': 0.27979947647514, '7-9': 0.20754606552556637, '8-9': 0.3186457177691013}

    # 2017-2020
    # relevance_dict = {'0-1': 0.10912139092477707, '0-2': 0.34253248360752103, '0-3': 0.26994280904877227, '0-4': 0.05188256598459868, '0-5': 0.35898260871074394, '0-6': 0.24486721350156343, '0-7': 0.17183722853549022, '0-8': 0.4398975896408202, '0-9': 0.34572577339026517, '1-2': 0.17118614722435674, '1-3': 0.1207444844382587, '1-4': 0.07946014413577052, '1-5': 0.16416400009964632, '1-6': 0.16750915212230055, '1-7': 0.11382671469176968, '1-8': 0.19689404659822335, '1-9': 0.12503165045484058, '2-3': 0.3089165947950442, '2-4': 0.11533579378194893, '2-5': 0.39698948955491, '2-6': 0.3904962536399381, '2-7': 0.14419551058009009, '2-8': 0.4998317509332274, '2-9': 0.39979817719794614, '3-4': 0.11183511796459382, '3-5': 0.31872888975332736, '3-6': 0.2200949087088748, '3-7': 0.13350664305556975, '3-8': 0.5223823857554684, '3-9': 0.33260514029347527, '4-5': 0.06903564567237158, '4-6': 0.16307539085533307, '4-7': 0.032198422646357396, '4-8': 0.052586280345705484, '4-9': 0.23979600057920905, '5-6': 0.2688244351740297, '5-7': 0.3052044211443993, '5-8': 0.5458989555021061, '5-9': 0.3861242691981531, '6-7': 0.12443327066170112, '6-8': 0.387605847738702, '6-9': 0.30335014695050017, '7-8': 0.25692080031414766, '7-9': 0.1609934695489194, '8-9': 0.4928719556863781}


    nodes = [
        {"id": "0", "name": "ID1:Bioremediation", "symbolSize": 48.6, "itemStyle": {"normal": {"color": color_list[0]}}},  # name需要替换成主题的名称（董老师给的）
        {"id": "1", "name": "ID2:Mechanism of mycorrhizal symbiosis", "symbolSize": 69.0, "itemStyle": {"normal": {"color": color_list[1]}}},
        {"id": "2", "name": "ID3:Field production1", "symbolSize": 29.5, "itemStyle": {"normal": {"color": color_list[2]}}},
        {"id": "3", "name": "ID4:Insect ecology", "symbolSize": 41.7, "itemStyle": {"normal": {"color": color_list[3]}}},
        {"id": "4", "name": "ID5:Feeding value", "symbolSize": 56.2, "itemStyle": {"normal": {"color": color_list[4]}}},
        {"id": "5", "name": "ID6:Seed treatment", "symbolSize": 33.6, "itemStyle": {"normal": {"color": color_list[5]}}},
        {"id": "6", "name": "ID7:Bioactive ingredients", "symbolSize": 43.3, "itemStyle": {"normal": {"color": color_list[6]}}},
        {"id": "7", "name": "ID8:Field production2", "symbolSize": 61.5, "itemStyle": {"normal": {"color": color_list[7]}}},
        {"id": "8", "name": "ID9:Resistance to abiotic stress", "symbolSize": 54.9, "itemStyle": {"normal": {"color": color_list[8]}}},
        {"id": "9", "name": "ID10:Protein genomics", "symbolSize": 62.8, "itemStyle": {"normal": {"color": color_list[9]}}},
    ]

    links = []
    index = 0

    avg_dict = sum(relevance_dict.values())/len(relevance_dict)
    max_dict = max(relevance_dict.values())
    min_dict = min(relevance_dict.values())


    for key, value in relevance_dict.items():
        # if value > 0.3:  # 设置阈值
        one_link = {}
        one_link['id'] = str(index)
        one_link['source'] = key.split("-")[0]
        one_link['target'] = key.split("-")[1]
        # one_link['lineStyle'] = {"width": value*8, "opacity": 0.6}   # 没有归一化
        one_link['lineStyle'] = {"width": (value-avg_dict)/(max_dict-min_dict)*15, "opacity": 0.6}   # 归一化后
        # one_link['value'] = str(row['关系label']) + "-" + row['关系名称'] + " : " + str(row['关系排序最终得分'])
        links.append(one_link)

    c = (
        Graph()
            .add("", nodes, links, repulsion=8000, is_draggable=True) # , layout="circular")
            .set_global_opts(title_opts=opts.TitleOpts(title="主题分布图"))
            .render(save_root + "9-主题分布图.html")
    )

# 10-主题演化桑基图
def topic_evolution():
    from pyecharts.charts import Sankey

    # 专家对主题聚类的命名结果
    # 中文版
    topic_name = {0:"1-生长发育与生物合成调控", 1: "1-生物修复", 2: "1-抗非生物胁迫", 3: "1-饲料营养成分", 4: "1-饲养价值",
                  5: "1-菌根共生机制研究", 6:"1-遗传多样性研究", 7: "1-其他", 8: "1-田间生产与环境影响", 9: "1-昆虫生态",          # 2009-2012
                  10: "2-其他1", 11: "2-饲养价值", 12: "2-其他2", 13: "2-生长发育与生物合成调控", 14: "2-种子处理",
                  15: "2-菌根共生机制研究", 16: "2-遗传多样性研究", 17: "2-昆虫生态", 18: "2-其他3", 19: "2-抗非生物胁迫",         # 2013-2016
                  20: "3-种子处理", 21: "3-生物活性成分", 22: "3-病毒与昆虫生态", 23: "3-生物修复", 24: "3-菌根共生机制研究",
                  25: "3-青贮发酵及饲料品质", 26: "3-遗传多样性研究", 27: "3-饲养价值", 28: "3-田间生产", 29: "3-抗非生物胁迫"}
        # ,    # 2017-2020
        #           30: "生物修复", 31: "菌根共生机制研究", 32: "田间生产", 33: "昆虫生态", 34: "饲养价值",
        #           35: "种子处理", 36: "生物活性成分", 37: "田间生产", 38: "抗非生物胁迫", 39: "其他"}                 # all

    # 英文版
    topic_name = {0:"1-Growth and synthesis regulation", 1: "1-Bioremediation", 2: "1-Resistance to abiotic stress", 3: "1-Feed nutrition", 4: "1-Feeding value",
                  5: "1-Mechanism of mycorrhizal symbiosis", 6:"1-Genetic diversity research", 7: "1-Cannot name exactly", 8: "1-Field production and environmental impact", 9: "1-Insect ecology",          # 2009-2012
                  10: "2-Cannot name exactly1", 11: "2-Feeding value", 12: "2-Cannot name exactly2", 13: "2-Growth and synthesis regulation", 14: "2-Seed treatment",
                  15: "2-Mechanism of mycorrhizal symbiosis", 16: "2-Genetic diversity research", 17: "2-Insect ecology", 18: "2-Cannot name exactly3", 19: "2-Resistance to abiotic stress",         # 2013-2016
                  20: "3-Seed treatment", 21: "3-Biologically active ingredients", 22: "3-Virus and insect ecology", 23: "3-Bioremediation", 24: "3-Mechanism of mycorrhizal symbiosis",
                  25: "3-Silage fermentation and feed quality", 26: "3-Genetic diversity research", 27: "3-Feeding value", 28: "3-Field production", 29: "3-Resistance to abiotic stress"}



    nodes = [ {"name": i} for i in list(topic_name.values())]

    # 0.15
    # links = [{'source': '1-生长发育与生物合成调控', 'target': '2-其他1', 'value': 13.04289522595014, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-生长发育与生物合成调控', 'target': '2-饲养价值', 'value': 5.347046091321203, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-生长发育与生物合成调控', 'target': '2-其他2', 'value': 20.835293526583648, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-生长发育与生物合成调控', 'target': '2-生长发育与生物合成调控', 'value': 8.92791442932558, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-生长发育与生物合成调控', 'target': '2-种子处理', 'value': 13.724875819428853, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-生长发育与生物合成调控', 'target': '2-菌根共生机制研究', 'value': 4.139875618764864, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-生长发育与生物合成调控', 'target': '2-遗传多样性研究', 'value': 40.258863610408575, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '1-生长发育与生物合成调控', 'target': '2-昆虫生态', 'value': 18.359357701549442, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-生长发育与生物合成调控', 'target': '2-其他3', 'value': 11.607317979976028, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-生长发育与生物合成调控', 'target': '2-抗非生物胁迫', 'value': 11.75655999669167, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-生物修复', 'target': '2-其他1', 'value': 12.78817285181044, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-生物修复', 'target': '2-饲养价值', 'value': 8.021376134925777, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-生物修复', 'target': '2-其他2', 'value': 19.55267997528968, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-生物修复', 'target': '2-生长发育与生物合成调控', 'value': 2.2513313661549237, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-生物修复', 'target': '2-种子处理', 'value': 23.69707125803412, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '1-生物修复', 'target': '2-菌根共生机制研究', 'value': 4.748361976854138, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-生物修复', 'target': '2-遗传多样性研究', 'value': 10.435172061055354, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-生物修复', 'target': '2-昆虫生态', 'value': 12.157430926383686, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-生物修复', 'target': '2-其他3', 'value': 22.09146524274016, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '1-生物修复', 'target': '2-抗非生物胁迫', 'value': 15.256938206751705, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-抗非生物胁迫', 'target': '2-其他1', 'value': 10.853284563042335, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-抗非生物胁迫', 'target': '2-饲养价值', 'value': 7.005959416450491, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-抗非生物胁迫', 'target': '2-其他2', 'value': 19.067424643417112, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-抗非生物胁迫', 'target': '2-生长发育与生物合成调控', 'value': 4.7873377533123325, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-抗非生物胁迫', 'target': '2-种子处理', 'value': 16.068109414186292, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-抗非生物胁迫', 'target': '2-菌根共生机制研究', 'value': 7.129483965959265, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-抗非生物胁迫', 'target': '2-遗传多样性研究', 'value': 10.302642842221262, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-抗非生物胁迫', 'target': '2-昆虫生态', 'value': 10.2087965306567, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-抗非生物胁迫', 'target': '2-其他3', 'value': 16.174648046776838, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-抗非生物胁迫', 'target': '2-抗非生物胁迫', 'value': 41.40231282397738, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '1-饲料营养成分', 'target': '2-其他1', 'value': 15.183714200306255, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-饲料营养成分', 'target': '2-饲养价值', 'value': 14.076670121098621, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-饲料营养成分', 'target': '2-其他2', 'value': 19.71285699894183, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '1-饲料营养成分', 'target': '2-生长发育与生物合成调控', 'value': 2.665881883748569, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-饲料营养成分', 'target': '2-种子处理', 'value': 20.329404069043395, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '1-饲料营养成分', 'target': '2-菌根共生机制研究', 'value': 1.3997164120698031, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-饲料营养成分', 'target': '2-遗传多样性研究', 'value': 9.603611348713256, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-饲料营养成分', 'target': '2-昆虫生态', 'value': 10.468907683358792, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-饲料营养成分', 'target': '2-其他3', 'value': 13.088546376097275, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-饲料营养成分', 'target': '2-抗非生物胁迫', 'value': 11.470690906622211, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-饲养价值', 'target': '2-其他1', 'value': 21.812307300151264, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-饲养价值', 'target': '2-饲养价值', 'value': 56.116820569159216, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '1-饲养价值', 'target': '2-其他2', 'value': 15.864790946051, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-饲养价值', 'target': '2-生长发育与生物合成调控', 'value': 2.1125442951147817, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-饲养价值', 'target': '2-种子处理', 'value': 22.64399521463607, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-饲养价值', 'target': '2-菌根共生机制研究', 'value': 3.150606312076271, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-饲养价值', 'target': '2-遗传多样性研究', 'value': 7.880126248903415, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-饲养价值', 'target': '2-昆虫生态', 'value': 9.64018604600679, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-饲养价值', 'target': '2-其他3', 'value': 13.428323767350351, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-饲养价值', 'target': '2-抗非生物胁迫', 'value': 10.35029930055084, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-菌根共生机制研究', 'target': '2-其他1', 'value': 6.961692043997001, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-菌根共生机制研究', 'target': '2-饲养价值', 'value': 2.312039167831921, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-菌根共生机制研究', 'target': '2-其他2', 'value': 2.348599875212804, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-菌根共生机制研究', 'target': '2-生长发育与生物合成调控', 'value': 23.871681963364562, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-菌根共生机制研究', 'target': '2-种子处理', 'value': 6.1622508633423, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-菌根共生机制研究', 'target': '2-菌根共生机制研究', 'value': 85.11129516684034, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '1-菌根共生机制研究', 'target': '2-遗传多样性研究', 'value': 10.466816574554901, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-菌根共生机制研究', 'target': '2-昆虫生态', 'value': 3.023547558360073, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-菌根共生机制研究', 'target': '2-其他3', 'value': 13.108715381451917, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-菌根共生机制研究', 'target': '2-抗非生物胁迫', 'value': 8.633361405044214, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-遗传多样性研究', 'target': '2-其他1', 'value': 4.464158318142111, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-遗传多样性研究', 'target': '2-饲养价值', 'value': 4.988804577529551, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-遗传多样性研究', 'target': '2-其他2', 'value': 6.357586163583757, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-遗传多样性研究', 'target': '2-生长发育与生物合成调控', 'value': 94.19277867851126, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '1-遗传多样性研究', 'target': '2-种子处理', 'value': 10.95735172490792, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-遗传多样性研究', 'target': '2-菌根共生机制研究', 'value': 28.36892071498293, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-遗传多样性研究', 'target': '2-遗传多样性研究', 'value': 35.346854397109574, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '1-遗传多样性研究', 'target': '2-昆虫生态', 'value': 4.830808235634747, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-遗传多样性研究', 'target': '2-其他3', 'value': 3.744796968259628, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-遗传多样性研究', 'target': '2-抗非生物胁迫', 'value': 18.747940221338528, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-其他', 'target': '2-其他1', 'value': 40.698130381313135, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '1-其他', 'target': '2-饲养价值', 'value': 13.721287561384619, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-其他', 'target': '2-其他2', 'value': 24.706009278140556, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '1-其他', 'target': '2-生长发育与生物合成调控', 'value': 2.3510245421930356, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-其他', 'target': '2-种子处理', 'value': 16.72540665509428, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-其他', 'target': '2-菌根共生机制研究', 'value': 2.691266245653703, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-其他', 'target': '2-遗传多样性研究', 'value': 11.734537917735466, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-其他', 'target': '2-昆虫生态', 'value': 11.91077852658844, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-其他', 'target': '2-其他3', 'value': 13.313383592100344, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-其他', 'target': '2-抗非生物胁迫', 'value': 11.14817529979644, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-田间生产与环境影响', 'target': '2-其他1', 'value': 19.57791225828202, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-田间生产与环境影响', 'target': '2-饲养价值', 'value': 9.33294103051548, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-田间生产与环境影响', 'target': '2-其他2', 'value': 19.591491920924078, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-田间生产与环境影响', 'target': '2-生长发育与生物合成调控', 'value': 1.044729921900024, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-田间生产与环境影响', 'target': '2-种子处理', 'value': 16.723783712887855, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-田间生产与环境影响', 'target': '2-菌根共生机制研究', 'value': 4.444497173227017, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-田间生产与环境影响', 'target': '2-遗传多样性研究', 'value': 10.117647586687152, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-田间生产与环境影响', 'target': '2-昆虫生态', 'value': 12.656776140252838, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-田间生产与环境影响', 'target': '2-其他3', 'value': 33.77466507640923, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '1-田间生产与环境影响', 'target': '2-抗非生物胁迫', 'value': 12.735555178914307, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-昆虫生态', 'target': '2-其他1', 'value': 11.842525414567758, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-昆虫生态', 'target': '2-饲养价值', 'value': 5.399860128906238, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-昆虫生态', 'target': '2-其他2', 'value': 16.695683749926726, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '1-昆虫生态', 'target': '2-生长发育与生物合成调控', 'value': 1.654434659091319, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-昆虫生态', 'target': '2-种子处理', 'value': 12.580217579562186, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-昆虫生态', 'target': '2-菌根共生机制研究', 'value': 1.3824033311344828, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-昆虫生态', 'target': '2-遗传多样性研究', 'value': 13.72224653723773, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-昆虫生态', 'target': '2-昆虫生态', 'value': 23.660447832610007, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '1-昆虫生态', 'target': '2-其他3', 'value': 10.815889711227046, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-昆虫生态', 'target': '2-抗非生物胁迫', 'value': 9.246291055736512, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-其他1', 'target': '3-种子处理', 'value': 10.702257286669907, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-其他1', 'target': '3-生物活性成分', 'value': 29.906096882695312, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '2-其他1', 'target': '3-病毒与昆虫生态', 'value': 15.276749223743607, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-其他1', 'target': '3-生物修复', 'value': 12.115880162609837, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-其他1', 'target': '3-菌根共生机制研究', 'value': 2.786561477117648, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-其他1', 'target': '3-青贮发酵及饲料品质', 'value': 16.081385781939105, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-其他1', 'target': '3-遗传多样性研究', 'value': 11.846425798163374, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-其他1', 'target': '3-饲养价值', 'value': 8.093214241441276, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-其他1', 'target': '3-田间生产', 'value': 24.51527827588873, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '2-其他1', 'target': '3-抗非生物胁迫', 'value': 11.67615086973122, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-饲养价值', 'target': '3-种子处理', 'value': 13.734832212062349, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-饲养价值', 'target': '3-生物活性成分', 'value': 13.073499861073312, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-饲养价值', 'target': '3-病毒与昆虫生态', 'value': 11.420201114303302, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-饲养价值', 'target': '3-生物修复', 'value': 10.464467615386665, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-饲养价值', 'target': '3-菌根共生机制研究', 'value': 2.3763027553501743, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-饲养价值', 'target': '3-青贮发酵及饲料品质', 'value': 30.68474877577769, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '2-饲养价值', 'target': '3-遗传多样性研究', 'value': 9.079669512721598, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-饲养价值', 'target': '3-饲养价值', 'value': 59.628186402781594, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '2-饲养价值', 'target': '3-田间生产', 'value': 20.977682940526986, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-饲养价值', 'target': '3-抗非生物胁迫', 'value': 12.560408810016359, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-其他2', 'target': '3-种子处理', 'value': 17.667101231440025, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-其他2', 'target': '3-生物活性成分', 'value': 6.585368716093608, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-其他2', 'target': '3-病毒与昆虫生态', 'value': 16.263592323502937, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-其他2', 'target': '3-生物修复', 'value': 11.377447234765384, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-其他2', 'target': '3-菌根共生机制研究', 'value': 1.9993199731593474, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-其他2', 'target': '3-青贮发酵及饲料品质', 'value': 16.489234877549332, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-其他2', 'target': '3-遗传多样性研究', 'value': 20.11604105846514, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-其他2', 'target': '3-饲养价值', 'value': 7.657080597740964, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-其他2', 'target': '3-田间生产', 'value': 25.82115117115067, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '2-其他2', 'target': '3-抗非生物胁迫', 'value': 17.023662816132582, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-生长发育与生物合成调控', 'target': '3-种子处理', 'value': 9.108428820092017, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-生长发育与生物合成调控', 'target': '3-生物活性成分', 'value': 8.667049181731453, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-生长发育与生物合成调控', 'target': '3-病毒与昆虫生态', 'value': 16.389906159247197, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-生长发育与生物合成调控', 'target': '3-生物修复', 'value': 5.883969044362244, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-生长发育与生物合成调控', 'target': '3-菌根共生机制研究', 'value': 119.43973463696092, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '2-生长发育与生物合成调控', 'target': '3-青贮发酵及饲料品质', 'value': 9.486955780674975, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-生长发育与生物合成调控', 'target': '3-遗传多样性研究', 'value': 23.786903115901087, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-生长发育与生物合成调控', 'target': '3-饲养价值', 'value': 5.24725543936518, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-生长发育与生物合成调控', 'target': '3-田间生产', 'value': 5.306257653334967, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-生长发育与生物合成调控', 'target': '3-抗非生物胁迫', 'value': 42.68354016832993, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '2-种子处理', 'target': '3-种子处理', 'value': 28.97757726094021, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '2-种子处理', 'target': '3-生物活性成分', 'value': 7.389785264002699, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-种子处理', 'target': '3-病毒与昆虫生态', 'value': 17.266784055551177, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-种子处理', 'target': '3-生物修复', 'value': 13.64114046752461, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-种子处理', 'target': '3-菌根共生机制研究', 'value': 3.729588780615047, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-种子处理', 'target': '3-青贮发酵及饲料品质', 'value': 30.056242720655515, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '2-种子处理', 'target': '3-遗传多样性研究', 'value': 12.063951083199132, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-种子处理', 'target': '3-饲养价值', 'value': 9.4883844886336, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-种子处理', 'target': '3-田间生产', 'value': 22.048459120545548, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-种子处理', 'target': '3-抗非生物胁迫', 'value': 17.33808675833248, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-菌根共生机制研究', 'target': '3-种子处理', 'value': 7.131633476677254, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-菌根共生机制研究', 'target': '3-生物活性成分', 'value': 9.90664586274734, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-菌根共生机制研究', 'target': '3-病毒与昆虫生态', 'value': 10.091085002412976, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-菌根共生机制研究', 'target': '3-生物修复', 'value': 37.552017516370526, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '2-菌根共生机制研究', 'target': '3-菌根共生机制研究', 'value': 77.77458133528617, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '2-菌根共生机制研究', 'target': '3-青贮发酵及饲料品质', 'value': 9.593068106433295, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-菌根共生机制研究', 'target': '3-遗传多样性研究', 'value': 7.387677405282318, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-菌根共生机制研究', 'target': '3-饲养价值', 'value': 3.6408719696521077, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-菌根共生机制研究', 'target': '3-田间生产', 'value': 10.61368731512471, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-菌根共生机制研究', 'target': '3-抗非生物胁迫', 'value': 15.308732010013303, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-遗传多样性研究', 'target': '3-种子处理', 'value': 11.968696867293092, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-遗传多样性研究', 'target': '3-生物活性成分', 'value': 8.291012783016301, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-遗传多样性研究', 'target': '3-病毒与昆虫生态', 'value': 29.657537801581952, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '2-遗传多样性研究', 'target': '3-生物修复', 'value': 12.126494637897693, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-遗传多样性研究', 'target': '3-菌根共生机制研究', 'value': 16.521293458470183, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-遗传多样性研究', 'target': '3-青贮发酵及饲料品质', 'value': 12.980220088195004, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-遗传多样性研究', 'target': '3-遗传多样性研究', 'value': 37.885693655052414, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '2-遗传多样性研究', 'target': '3-饲养价值', 'value': 4.863429948960535, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-遗传多样性研究', 'target': '3-田间生产', 'value': 16.803385662552454, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-遗传多样性研究', 'target': '3-抗非生物胁迫', 'value': 15.902235096980368, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-昆虫生态', 'target': '3-种子处理', 'value': 9.397321996201539, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-昆虫生态', 'target': '3-生物活性成分', 'value': 6.721257510490792, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-昆虫生态', 'target': '3-病毒与昆虫生态', 'value': 24.599159271097623, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '2-昆虫生态', 'target': '3-生物修复', 'value': 9.01574387476123, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-昆虫生态', 'target': '3-菌根共生机制研究', 'value': 2.142379424834374, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-昆虫生态', 'target': '3-青贮发酵及饲料品质', 'value': 10.628160272858656, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-昆虫生态', 'target': '3-遗传多样性研究', 'value': 12.477812175325031, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-昆虫生态', 'target': '3-饲养价值', 'value': 4.177956874210419, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-昆虫生态', 'target': '3-田间生产', 'value': 14.046679131623094, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-昆虫生态', 'target': '3-抗非生物胁迫', 'value': 9.793529468597242, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-其他3', 'target': '3-种子处理', 'value': 15.485655058454093, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-其他3', 'target': '3-生物活性成分', 'value': 5.850759740932151, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-其他3', 'target': '3-病毒与昆虫生态', 'value': 15.923207235747538, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-其他3', 'target': '3-生物修复', 'value': 37.724864413159914, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '2-其他3', 'target': '3-菌根共生机制研究', 'value': 2.8435355144822214, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-其他3', 'target': '3-青贮发酵及饲料品质', 'value': 16.825401612965944, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-其他3', 'target': '3-遗传多样性研究', 'value': 11.549674550750312, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-其他3', 'target': '3-饲养价值', 'value': 7.829834466026031, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-其他3', 'target': '3-田间生产', 'value': 33.64911066753503, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '2-其他3', 'target': '3-抗非生物胁迫', 'value': 16.317956739946776, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-抗非生物胁迫', 'target': '3-种子处理', 'value': 20.653796885861674, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-抗非生物胁迫', 'target': '3-生物活性成分', 'value': 6.77029247995077, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-抗非生物胁迫', 'target': '3-病毒与昆虫生态', 'value': 19.804100989974746, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-抗非生物胁迫', 'target': '3-生物修复', 'value': 18.6295247295276, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-抗非生物胁迫', 'target': '3-菌根共生机制研究', 'value': 9.115322857549444, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-抗非生物胁迫', 'target': '3-青贮发酵及饲料品质', 'value': 18.871794235986343, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-抗非生物胁迫', 'target': '3-遗传多样性研究', 'value': 15.192347119484827, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-抗非生物胁迫', 'target': '3-饲养价值', 'value': 8.101224855923986, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-抗非生物胁迫', 'target': '3-田间生产', 'value': 25.78445231588425, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-抗非生物胁迫', 'target': '3-抗非生物胁迫', 'value': 56.077143529856336, 'lineStyle': {'color': 'source', 'opacity': 0.2}}]
    # links = [{'source': '1-Growth and synthesis regulation', 'target': '2-Cannot name exactly1', 'value': 13.04289522595014, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Growth and synthesis regulation', 'target': '2-Feeding value', 'value': 5.347046091321203, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Growth and synthesis regulation', 'target': '2-Cannot name exactly2', 'value': 20.835293526583648, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Growth and synthesis regulation', 'target': '2-Growth and synthesis regulation', 'value': 8.92791442932558, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Growth and synthesis regulation', 'target': '2-Seed treatment', 'value': 13.724875819428853, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Growth and synthesis regulation', 'target': '2-Mechanism of mycorrhizal symbiosis', 'value': 4.139875618764864, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Growth and synthesis regulation', 'target': '2-Genetic diversity research', 'value': 40.258863610408575, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '1-Growth and synthesis regulation', 'target': '2-Insect ecology', 'value': 18.359357701549442, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Growth and synthesis regulation', 'target': '2-Cannot name exactly3', 'value': 11.607317979976028, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Growth and synthesis regulation', 'target': '2-Resistance to abiotic stress', 'value': 11.75655999669167, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Bioremediation', 'target': '2-Cannot name exactly1', 'value': 12.78817285181044, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Bioremediation', 'target': '2-Feeding value', 'value': 8.021376134925777, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Bioremediation', 'target': '2-Cannot name exactly2', 'value': 19.55267997528968, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Bioremediation', 'target': '2-Growth and synthesis regulation', 'value': 2.2513313661549237, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Bioremediation', 'target': '2-Seed treatment', 'value': 23.69707125803412, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '1-Bioremediation', 'target': '2-Mechanism of mycorrhizal symbiosis', 'value': 4.748361976854138, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Bioremediation', 'target': '2-Genetic diversity research', 'value': 10.435172061055354, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Bioremediation', 'target': '2-Insect ecology', 'value': 12.157430926383686, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Bioremediation', 'target': '2-Cannot name exactly3', 'value': 22.09146524274016, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '1-Bioremediation', 'target': '2-Resistance to abiotic stress', 'value': 15.256938206751705, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Resistance to abiotic stress', 'target': '2-Cannot name exactly1', 'value': 10.853284563042335, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Resistance to abiotic stress', 'target': '2-Feeding value', 'value': 7.005959416450491, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Resistance to abiotic stress', 'target': '2-Cannot name exactly2', 'value': 19.067424643417112, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Resistance to abiotic stress', 'target': '2-Growth and synthesis regulation', 'value': 4.7873377533123325, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Resistance to abiotic stress', 'target': '2-Seed treatment', 'value': 16.068109414186292, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Resistance to abiotic stress', 'target': '2-Mechanism of mycorrhizal symbiosis', 'value': 7.129483965959265, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Resistance to abiotic stress', 'target': '2-Genetic diversity research', 'value': 10.302642842221262, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Resistance to abiotic stress', 'target': '2-Insect ecology', 'value': 10.2087965306567, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Resistance to abiotic stress', 'target': '2-Cannot name exactly3', 'value': 16.174648046776838, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Resistance to abiotic stress', 'target': '2-Resistance to abiotic stress', 'value': 41.40231282397738, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '1-Feed nutrition', 'target': '2-Cannot name exactly1', 'value': 15.183714200306255, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Feed nutrition', 'target': '2-Feeding value', 'value': 14.076670121098621, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Feed nutrition', 'target': '2-Cannot name exactly2', 'value': 19.71285699894183, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '1-Feed nutrition', 'target': '2-Growth and synthesis regulation', 'value': 2.665881883748569, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Feed nutrition', 'target': '2-Seed treatment', 'value': 20.329404069043395, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '1-Feed nutrition', 'target': '2-Mechanism of mycorrhizal symbiosis', 'value': 1.3997164120698031, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Feed nutrition', 'target': '2-Genetic diversity research', 'value': 9.603611348713256, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Feed nutrition', 'target': '2-Insect ecology', 'value': 10.468907683358792, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Feed nutrition', 'target': '2-Cannot name exactly3', 'value': 13.088546376097275, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Feed nutrition', 'target': '2-Resistance to abiotic stress', 'value': 11.470690906622211, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Feeding value', 'target': '2-Cannot name exactly1', 'value': 21.812307300151264, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Feeding value', 'target': '2-Feeding value', 'value': 56.116820569159216, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '1-Feeding value', 'target': '2-Cannot name exactly2', 'value': 15.864790946051, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Feeding value', 'target': '2-Growth and synthesis regulation', 'value': 2.1125442951147817, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Feeding value', 'target': '2-Seed treatment', 'value': 22.64399521463607, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Feeding value', 'target': '2-Mechanism of mycorrhizal symbiosis', 'value': 3.150606312076271, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Feeding value', 'target': '2-Genetic diversity research', 'value': 7.880126248903415, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Feeding value', 'target': '2-Insect ecology', 'value': 9.64018604600679, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Feeding value', 'target': '2-Cannot name exactly3', 'value': 13.428323767350351, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Feeding value', 'target': '2-Resistance to abiotic stress', 'value': 10.35029930055084, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Mechanism of mycorrhizal symbiosis', 'target': '2-Cannot name exactly1', 'value': 6.961692043997001, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Mechanism of mycorrhizal symbiosis', 'target': '2-Feeding value', 'value': 2.312039167831921, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Mechanism of mycorrhizal symbiosis', 'target': '2-Cannot name exactly2', 'value': 2.348599875212804, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Mechanism of mycorrhizal symbiosis', 'target': '2-Growth and synthesis regulation', 'value': 23.871681963364562, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Mechanism of mycorrhizal symbiosis', 'target': '2-Seed treatment', 'value': 6.1622508633423, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Mechanism of mycorrhizal symbiosis', 'target': '2-Mechanism of mycorrhizal symbiosis', 'value': 85.11129516684034, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '1-Mechanism of mycorrhizal symbiosis', 'target': '2-Genetic diversity research', 'value': 10.466816574554901, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Mechanism of mycorrhizal symbiosis', 'target': '2-Insect ecology', 'value': 3.023547558360073, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Mechanism of mycorrhizal symbiosis', 'target': '2-Cannot name exactly3', 'value': 13.108715381451917, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Mechanism of mycorrhizal symbiosis', 'target': '2-Resistance to abiotic stress', 'value': 8.633361405044214, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Genetic diversity research', 'target': '2-Cannot name exactly1', 'value': 4.464158318142111, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Genetic diversity research', 'target': '2-Feeding value', 'value': 4.988804577529551, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Genetic diversity research', 'target': '2-Cannot name exactly2', 'value': 6.357586163583757, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Genetic diversity research', 'target': '2-Growth and synthesis regulation', 'value': 94.19277867851126, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '1-Genetic diversity research', 'target': '2-Seed treatment', 'value': 10.95735172490792, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Genetic diversity research', 'target': '2-Mechanism of mycorrhizal symbiosis', 'value': 28.36892071498293, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Genetic diversity research', 'target': '2-Genetic diversity research', 'value': 35.346854397109574, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '1-Genetic diversity research', 'target': '2-Insect ecology', 'value': 4.830808235634747, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Genetic diversity research', 'target': '2-Cannot name exactly3', 'value': 3.744796968259628, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Genetic diversity research', 'target': '2-Resistance to abiotic stress', 'value': 18.747940221338528, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Cannot name exactly', 'target': '2-Cannot name exactly1', 'value': 40.698130381313135, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '1-Cannot name exactly', 'target': '2-Feeding value', 'value': 13.721287561384619, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Cannot name exactly', 'target': '2-Cannot name exactly2', 'value': 24.706009278140556, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '1-Cannot name exactly', 'target': '2-Growth and synthesis regulation', 'value': 2.3510245421930356, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Cannot name exactly', 'target': '2-Seed treatment', 'value': 16.72540665509428, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Cannot name exactly', 'target': '2-Mechanism of mycorrhizal symbiosis', 'value': 2.691266245653703, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Cannot name exactly', 'target': '2-Genetic diversity research', 'value': 11.734537917735466, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Cannot name exactly', 'target': '2-Insect ecology', 'value': 11.91077852658844, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Cannot name exactly', 'target': '2-Cannot name exactly3', 'value': 13.313383592100344, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Cannot name exactly', 'target': '2-Resistance to abiotic stress', 'value': 11.14817529979644, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Field production and environmental impact', 'target': '2-Cannot name exactly1', 'value': 19.57791225828202, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Field production and environmental impact', 'target': '2-Feeding value', 'value': 9.33294103051548, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Field production and environmental impact', 'target': '2-Cannot name exactly2', 'value': 19.591491920924078, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Field production and environmental impact', 'target': '2-Growth and synthesis regulation', 'value': 1.044729921900024, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Field production and environmental impact', 'target': '2-Seed treatment', 'value': 16.723783712887855, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Field production and environmental impact', 'target': '2-Mechanism of mycorrhizal symbiosis', 'value': 4.444497173227017, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Field production and environmental impact', 'target': '2-Genetic diversity research', 'value': 10.117647586687152, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Field production and environmental impact', 'target': '2-Insect ecology', 'value': 12.656776140252838, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Field production and environmental impact', 'target': '2-Cannot name exactly3', 'value': 33.77466507640923, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '1-Field production and environmental impact', 'target': '2-Resistance to abiotic stress', 'value': 12.735555178914307, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Insect ecology', 'target': '2-Cannot name exactly1', 'value': 11.842525414567758, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Insect ecology', 'target': '2-Feeding value', 'value': 5.399860128906238, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Insect ecology', 'target': '2-Cannot name exactly2', 'value': 16.695683749926726, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '1-Insect ecology', 'target': '2-Growth and synthesis regulation', 'value': 1.654434659091319, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Insect ecology', 'target': '2-Seed treatment', 'value': 12.580217579562186, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Insect ecology', 'target': '2-Mechanism of mycorrhizal symbiosis', 'value': 1.3824033311344828, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Insect ecology', 'target': '2-Genetic diversity research', 'value': 13.72224653723773, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Insect ecology', 'target': '2-Insect ecology', 'value': 23.660447832610007, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '1-Insect ecology', 'target': '2-Cannot name exactly3', 'value': 10.815889711227046, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Insect ecology', 'target': '2-Resistance to abiotic stress', 'value': 9.246291055736512, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Cannot name exactly1', 'target': '3-Seed treatment', 'value': 10.702257286669907, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Cannot name exactly1', 'target': '3-Biologically active ingredients', 'value': 29.906096882695312, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '2-Cannot name exactly1', 'target': '3-Virus and insect ecology', 'value': 15.276749223743607, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Cannot name exactly1', 'target': '3-Bioremediation', 'value': 12.115880162609837, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Cannot name exactly1', 'target': '3-Mechanism of mycorrhizal symbiosis', 'value': 2.786561477117648, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Cannot name exactly1', 'target': '3-Silage fermentation and feed quality', 'value': 16.081385781939105, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Cannot name exactly1', 'target': '3-Genetic diversity research', 'value': 11.846425798163374, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Cannot name exactly1', 'target': '3-Feeding value', 'value': 8.093214241441276, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Cannot name exactly1', 'target': '3-Field production', 'value': 24.51527827588873, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '2-Cannot name exactly1', 'target': '3-Resistance to abiotic stress', 'value': 11.67615086973122, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Feeding value', 'target': '3-Seed treatment', 'value': 13.734832212062349, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Feeding value', 'target': '3-Biologically active ingredients', 'value': 13.073499861073312, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Feeding value', 'target': '3-Virus and insect ecology', 'value': 11.420201114303302, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Feeding value', 'target': '3-Bioremediation', 'value': 10.464467615386665, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Feeding value', 'target': '3-Mechanism of mycorrhizal symbiosis', 'value': 2.3763027553501743, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Feeding value', 'target': '3-Silage fermentation and feed quality', 'value': 30.68474877577769, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '2-Feeding value', 'target': '3-Genetic diversity research', 'value': 9.079669512721598, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Feeding value', 'target': '3-Feeding value', 'value': 59.628186402781594, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '2-Feeding value', 'target': '3-Field production', 'value': 20.977682940526986, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Feeding value', 'target': '3-Resistance to abiotic stress', 'value': 12.560408810016359, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Cannot name exactly2', 'target': '3-Seed treatment', 'value': 17.667101231440025, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Cannot name exactly2', 'target': '3-Biologically active ingredients', 'value': 6.585368716093608, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Cannot name exactly2', 'target': '3-Virus and insect ecology', 'value': 16.263592323502937, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Cannot name exactly2', 'target': '3-Bioremediation', 'value': 11.377447234765384, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Cannot name exactly2', 'target': '3-Mechanism of mycorrhizal symbiosis', 'value': 1.9993199731593474, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Cannot name exactly2', 'target': '3-Silage fermentation and feed quality', 'value': 16.489234877549332, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Cannot name exactly2', 'target': '3-Genetic diversity research', 'value': 20.11604105846514, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Cannot name exactly2', 'target': '3-Feeding value', 'value': 7.657080597740964, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Cannot name exactly2', 'target': '3-Field production', 'value': 25.82115117115067, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '2-Cannot name exactly2', 'target': '3-Resistance to abiotic stress', 'value': 17.023662816132582, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Growth and synthesis regulation', 'target': '3-Seed treatment', 'value': 9.108428820092017, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Growth and synthesis regulation', 'target': '3-Biologically active ingredients', 'value': 8.667049181731453, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Growth and synthesis regulation', 'target': '3-Virus and insect ecology', 'value': 16.389906159247197, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Growth and synthesis regulation', 'target': '3-Bioremediation', 'value': 5.883969044362244, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Growth and synthesis regulation', 'target': '3-Mechanism of mycorrhizal symbiosis', 'value': 119.43973463696092, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '2-Growth and synthesis regulation', 'target': '3-Silage fermentation and feed quality', 'value': 9.486955780674975, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Growth and synthesis regulation', 'target': '3-Genetic diversity research', 'value': 23.786903115901087, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Growth and synthesis regulation', 'target': '3-Feeding value', 'value': 5.24725543936518, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Growth and synthesis regulation', 'target': '3-Field production', 'value': 5.306257653334967, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Growth and synthesis regulation', 'target': '3-Resistance to abiotic stress', 'value': 42.68354016832993, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '2-Seed treatment', 'target': '3-Seed treatment', 'value': 28.97757726094021, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '2-Seed treatment', 'target': '3-Biologically active ingredients', 'value': 7.389785264002699, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Seed treatment', 'target': '3-Virus and insect ecology', 'value': 17.266784055551177, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Seed treatment', 'target': '3-Bioremediation', 'value': 13.64114046752461, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Seed treatment', 'target': '3-Mechanism of mycorrhizal symbiosis', 'value': 3.729588780615047, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Seed treatment', 'target': '3-Silage fermentation and feed quality', 'value': 30.056242720655515, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '2-Seed treatment', 'target': '3-Genetic diversity research', 'value': 12.063951083199132, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Seed treatment', 'target': '3-Feeding value', 'value': 9.4883844886336, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Seed treatment', 'target': '3-Field production', 'value': 22.048459120545548, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Seed treatment', 'target': '3-Resistance to abiotic stress', 'value': 17.33808675833248, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Mechanism of mycorrhizal symbiosis', 'target': '3-Seed treatment', 'value': 7.131633476677254, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Mechanism of mycorrhizal symbiosis', 'target': '3-Biologically active ingredients', 'value': 9.90664586274734, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Mechanism of mycorrhizal symbiosis', 'target': '3-Virus and insect ecology', 'value': 10.091085002412976, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Mechanism of mycorrhizal symbiosis', 'target': '3-Bioremediation', 'value': 37.552017516370526, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '2-Mechanism of mycorrhizal symbiosis', 'target': '3-Mechanism of mycorrhizal symbiosis', 'value': 77.77458133528617, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '2-Mechanism of mycorrhizal symbiosis', 'target': '3-Silage fermentation and feed quality', 'value': 9.593068106433295, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Mechanism of mycorrhizal symbiosis', 'target': '3-Genetic diversity research', 'value': 7.387677405282318, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Mechanism of mycorrhizal symbiosis', 'target': '3-Feeding value', 'value': 3.6408719696521077, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Mechanism of mycorrhizal symbiosis', 'target': '3-Field production', 'value': 10.61368731512471, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Mechanism of mycorrhizal symbiosis', 'target': '3-Resistance to abiotic stress', 'value': 15.308732010013303, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Genetic diversity research', 'target': '3-Seed treatment', 'value': 11.968696867293092, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Genetic diversity research', 'target': '3-Biologically active ingredients', 'value': 8.291012783016301, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Genetic diversity research', 'target': '3-Virus and insect ecology', 'value': 29.657537801581952, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '2-Genetic diversity research', 'target': '3-Bioremediation', 'value': 12.126494637897693, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Genetic diversity research', 'target': '3-Mechanism of mycorrhizal symbiosis', 'value': 16.521293458470183, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Genetic diversity research', 'target': '3-Silage fermentation and feed quality', 'value': 12.980220088195004, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Genetic diversity research', 'target': '3-Genetic diversity research', 'value': 37.885693655052414, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '2-Genetic diversity research', 'target': '3-Feeding value', 'value': 4.863429948960535, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Genetic diversity research', 'target': '3-Field production', 'value': 16.803385662552454, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Genetic diversity research', 'target': '3-Resistance to abiotic stress', 'value': 15.902235096980368, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Insect ecology', 'target': '3-Seed treatment', 'value': 9.397321996201539, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Insect ecology', 'target': '3-Biologically active ingredients', 'value': 6.721257510490792, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Insect ecology', 'target': '3-Virus and insect ecology', 'value': 24.599159271097623, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '2-Insect ecology', 'target': '3-Bioremediation', 'value': 9.01574387476123, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Insect ecology', 'target': '3-Mechanism of mycorrhizal symbiosis', 'value': 2.142379424834374, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Insect ecology', 'target': '3-Silage fermentation and feed quality', 'value': 10.628160272858656, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Insect ecology', 'target': '3-Genetic diversity research', 'value': 12.477812175325031, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Insect ecology', 'target': '3-Feeding value', 'value': 4.177956874210419, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Insect ecology', 'target': '3-Field production', 'value': 14.046679131623094, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Insect ecology', 'target': '3-Resistance to abiotic stress', 'value': 9.793529468597242, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Cannot name exactly3', 'target': '3-Seed treatment', 'value': 15.485655058454093, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Cannot name exactly3', 'target': '3-Biologically active ingredients', 'value': 5.850759740932151, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Cannot name exactly3', 'target': '3-Virus and insect ecology', 'value': 15.923207235747538, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Cannot name exactly3', 'target': '3-Bioremediation', 'value': 37.724864413159914, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '2-Cannot name exactly3', 'target': '3-Mechanism of mycorrhizal symbiosis', 'value': 2.8435355144822214, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Cannot name exactly3', 'target': '3-Silage fermentation and feed quality', 'value': 16.825401612965944, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Cannot name exactly3', 'target': '3-Genetic diversity research', 'value': 11.549674550750312, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Cannot name exactly3', 'target': '3-Feeding value', 'value': 7.829834466026031, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Cannot name exactly3', 'target': '3-Field production', 'value': 33.64911066753503, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '2-Cannot name exactly3', 'target': '3-Resistance to abiotic stress', 'value': 16.317956739946776, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Resistance to abiotic stress', 'target': '3-Seed treatment', 'value': 20.653796885861674, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Resistance to abiotic stress', 'target': '3-Biologically active ingredients', 'value': 6.77029247995077, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Resistance to abiotic stress', 'target': '3-Virus and insect ecology', 'value': 19.804100989974746, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Resistance to abiotic stress', 'target': '3-Bioremediation', 'value': 18.6295247295276, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Resistance to abiotic stress', 'target': '3-Mechanism of mycorrhizal symbiosis', 'value': 9.115322857549444, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Resistance to abiotic stress', 'target': '3-Silage fermentation and feed quality', 'value': 18.871794235986343, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Resistance to abiotic stress', 'target': '3-Genetic diversity research', 'value': 15.192347119484827, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Resistance to abiotic stress', 'target': '3-Feeding value', 'value': 8.101224855923986, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Resistance to abiotic stress', 'target': '3-Field production', 'value': 25.78445231588425, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Resistance to abiotic stress', 'target': '3-Resistance to abiotic stress', 'value': 56.077143529856336, 'lineStyle': {'color': 'source', 'opacity': 0.2}}]

    # 0.12
    # links = [{'source': '1-生长发育与生物合成调控', 'target': '2-其他1', 'value': 13.04289522595014, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-生长发育与生物合成调控', 'target': '2-饲养价值', 'value': 5.347046091321203, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-生长发育与生物合成调控', 'target': '2-其他2', 'value': 20.835293526583648, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '1-生长发育与生物合成调控', 'target': '2-生长发育与生物合成调控', 'value': 8.92791442932558, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-生长发育与生物合成调控', 'target': '2-种子处理', 'value': 13.724875819428853, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-生长发育与生物合成调控', 'target': '2-菌根共生机制研究', 'value': 4.139875618764864, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-生长发育与生物合成调控', 'target': '2-遗传多样性研究', 'value': 40.258863610408575, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '1-生长发育与生物合成调控', 'target': '2-昆虫生态', 'value': 18.359357701549442, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '1-生长发育与生物合成调控', 'target': '2-其他3', 'value': 11.607317979976028, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-生长发育与生物合成调控', 'target': '2-抗非生物胁迫', 'value': 11.75655999669167, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-生物修复', 'target': '2-其他1', 'value': 12.78817285181044, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-生物修复', 'target': '2-饲养价值', 'value': 8.021376134925777, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-生物修复', 'target': '2-其他2', 'value': 19.55267997528968, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '1-生物修复', 'target': '2-生长发育与生物合成调控', 'value': 2.2513313661549237, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-生物修复', 'target': '2-种子处理', 'value': 23.69707125803412, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '1-生物修复', 'target': '2-菌根共生机制研究', 'value': 4.748361976854138, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-生物修复', 'target': '2-遗传多样性研究', 'value': 10.435172061055354, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-生物修复', 'target': '2-昆虫生态', 'value': 12.157430926383686, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-生物修复', 'target': '2-其他3', 'value': 22.09146524274016, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '1-生物修复', 'target': '2-抗非生物胁迫', 'value': 15.256938206751705, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-抗非生物胁迫', 'target': '2-其他1', 'value': 10.853284563042335, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-抗非生物胁迫', 'target': '2-饲养价值', 'value': 7.005959416450491, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-抗非生物胁迫', 'target': '2-其他2', 'value': 19.067424643417112, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '1-抗非生物胁迫', 'target': '2-生长发育与生物合成调控', 'value': 4.7873377533123325, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-抗非生物胁迫', 'target': '2-种子处理', 'value': 16.068109414186292, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-抗非生物胁迫', 'target': '2-菌根共生机制研究', 'value': 7.129483965959265, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-抗非生物胁迫', 'target': '2-遗传多样性研究', 'value': 10.302642842221262, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-抗非生物胁迫', 'target': '2-昆虫生态', 'value': 10.2087965306567, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-抗非生物胁迫', 'target': '2-其他3', 'value': 16.174648046776838, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-抗非生物胁迫', 'target': '2-抗非生物胁迫', 'value': 41.40231282397738, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '1-饲料营养成分', 'target': '2-其他1', 'value': 15.183714200306255, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '1-饲料营养成分', 'target': '2-饲养价值', 'value': 14.076670121098621, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-饲料营养成分', 'target': '2-其他2', 'value': 19.71285699894183, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '1-饲料营养成分', 'target': '2-生长发育与生物合成调控', 'value': 2.665881883748569, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-饲料营养成分', 'target': '2-种子处理', 'value': 20.329404069043395, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '1-饲料营养成分', 'target': '2-菌根共生机制研究', 'value': 1.3997164120698031, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-饲料营养成分', 'target': '2-遗传多样性研究', 'value': 9.603611348713256, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-饲料营养成分', 'target': '2-昆虫生态', 'value': 10.468907683358792, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-饲料营养成分', 'target': '2-其他3', 'value': 13.088546376097275, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-饲料营养成分', 'target': '2-抗非生物胁迫', 'value': 11.470690906622211, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-饲养价值', 'target': '2-其他1', 'value': 21.812307300151264, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '1-饲养价值', 'target': '2-饲养价值', 'value': 56.116820569159216, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '1-饲养价值', 'target': '2-其他2', 'value': 15.864790946051, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-饲养价值', 'target': '2-生长发育与生物合成调控', 'value': 2.1125442951147817, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-饲养价值', 'target': '2-种子处理', 'value': 22.64399521463607, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '1-饲养价值', 'target': '2-菌根共生机制研究', 'value': 3.150606312076271, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-饲养价值', 'target': '2-遗传多样性研究', 'value': 7.880126248903415, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-饲养价值', 'target': '2-昆虫生态', 'value': 9.64018604600679, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-饲养价值', 'target': '2-其他3', 'value': 13.428323767350351, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-饲养价值', 'target': '2-抗非生物胁迫', 'value': 10.35029930055084, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-菌根共生机制研究', 'target': '2-其他1', 'value': 6.961692043997001, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-菌根共生机制研究', 'target': '2-饲养价值', 'value': 2.312039167831921, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-菌根共生机制研究', 'target': '2-其他2', 'value': 2.348599875212804, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-菌根共生机制研究', 'target': '2-生长发育与生物合成调控', 'value': 23.871681963364562, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '1-菌根共生机制研究', 'target': '2-种子处理', 'value': 6.1622508633423, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-菌根共生机制研究', 'target': '2-菌根共生机制研究', 'value': 85.11129516684034, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '1-菌根共生机制研究', 'target': '2-遗传多样性研究', 'value': 10.466816574554901, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-菌根共生机制研究', 'target': '2-昆虫生态', 'value': 3.023547558360073, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-菌根共生机制研究', 'target': '2-其他3', 'value': 13.108715381451917, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-菌根共生机制研究', 'target': '2-抗非生物胁迫', 'value': 8.633361405044214, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-遗传多样性研究', 'target': '2-其他1', 'value': 4.464158318142111, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-遗传多样性研究', 'target': '2-饲养价值', 'value': 4.988804577529551, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-遗传多样性研究', 'target': '2-其他2', 'value': 6.357586163583757, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-遗传多样性研究', 'target': '2-生长发育与生物合成调控', 'value': 94.19277867851126, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '1-遗传多样性研究', 'target': '2-种子处理', 'value': 10.95735172490792, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-遗传多样性研究', 'target': '2-菌根共生机制研究', 'value': 28.36892071498293, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '1-遗传多样性研究', 'target': '2-遗传多样性研究', 'value': 35.346854397109574, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '1-遗传多样性研究', 'target': '2-昆虫生态', 'value': 4.830808235634747, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-遗传多样性研究', 'target': '2-其他3', 'value': 3.744796968259628, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-遗传多样性研究', 'target': '2-抗非生物胁迫', 'value': 18.747940221338528, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-其他', 'target': '2-其他1', 'value': 40.698130381313135, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '1-其他', 'target': '2-饲养价值', 'value': 13.721287561384619, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-其他', 'target': '2-其他2', 'value': 24.706009278140556, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '1-其他', 'target': '2-生长发育与生物合成调控', 'value': 2.3510245421930356, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-其他', 'target': '2-种子处理', 'value': 16.72540665509428, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-其他', 'target': '2-菌根共生机制研究', 'value': 2.691266245653703, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-其他', 'target': '2-遗传多样性研究', 'value': 11.734537917735466, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-其他', 'target': '2-昆虫生态', 'value': 11.91077852658844, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-其他', 'target': '2-其他3', 'value': 13.313383592100344, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-其他', 'target': '2-抗非生物胁迫', 'value': 11.14817529979644, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-田间生产与环境影响', 'target': '2-其他1', 'value': 19.57791225828202, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '1-田间生产与环境影响', 'target': '2-饲养价值', 'value': 9.33294103051548, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-田间生产与环境影响', 'target': '2-其他2', 'value': 19.591491920924078, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '1-田间生产与环境影响', 'target': '2-生长发育与生物合成调控', 'value': 1.044729921900024, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-田间生产与环境影响', 'target': '2-种子处理', 'value': 16.723783712887855, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-田间生产与环境影响', 'target': '2-菌根共生机制研究', 'value': 4.444497173227017, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-田间生产与环境影响', 'target': '2-遗传多样性研究', 'value': 10.117647586687152, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-田间生产与环境影响', 'target': '2-昆虫生态', 'value': 12.656776140252838, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-田间生产与环境影响', 'target': '2-其他3', 'value': 33.77466507640923, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '1-田间生产与环境影响', 'target': '2-抗非生物胁迫', 'value': 12.735555178914307, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-昆虫生态', 'target': '2-其他1', 'value': 11.842525414567758, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-昆虫生态', 'target': '2-饲养价值', 'value': 5.399860128906238, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-昆虫生态', 'target': '2-其他2', 'value': 16.695683749926726, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '1-昆虫生态', 'target': '2-生长发育与生物合成调控', 'value': 1.654434659091319, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-昆虫生态', 'target': '2-种子处理', 'value': 12.580217579562186, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-昆虫生态', 'target': '2-菌根共生机制研究', 'value': 1.3824033311344828, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-昆虫生态', 'target': '2-遗传多样性研究', 'value': 13.72224653723773, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '1-昆虫生态', 'target': '2-昆虫生态', 'value': 23.660447832610007, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '1-昆虫生态', 'target': '2-其他3', 'value': 10.815889711227046, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-昆虫生态', 'target': '2-抗非生物胁迫', 'value': 9.246291055736512, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-其他1', 'target': '3-种子处理', 'value': 10.702257286669907, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-其他1', 'target': '3-生物活性成分', 'value': 29.906096882695312, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '2-其他1', 'target': '3-病毒与昆虫生态', 'value': 15.276749223743607, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-其他1', 'target': '3-生物修复', 'value': 12.115880162609837, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-其他1', 'target': '3-菌根共生机制研究', 'value': 2.786561477117648, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-其他1', 'target': '3-青贮发酵及饲料品质', 'value': 16.081385781939105, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-其他1', 'target': '3-遗传多样性研究', 'value': 11.846425798163374, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-其他1', 'target': '3-饲养价值', 'value': 8.093214241441276, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-其他1', 'target': '3-田间生产', 'value': 24.51527827588873, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '2-其他1', 'target': '3-抗非生物胁迫', 'value': 11.67615086973122, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-饲养价值', 'target': '3-种子处理', 'value': 13.734832212062349, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-饲养价值', 'target': '3-生物活性成分', 'value': 13.073499861073312, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-饲养价值', 'target': '3-病毒与昆虫生态', 'value': 11.420201114303302, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-饲养价值', 'target': '3-生物修复', 'value': 10.464467615386665, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-饲养价值', 'target': '3-菌根共生机制研究', 'value': 2.3763027553501743, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-饲养价值', 'target': '3-青贮发酵及饲料品质', 'value': 30.68474877577769, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '2-饲养价值', 'target': '3-遗传多样性研究', 'value': 9.079669512721598, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-饲养价值', 'target': '3-饲养价值', 'value': 59.628186402781594, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '2-饲养价值', 'target': '3-田间生产', 'value': 20.977682940526986, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-饲养价值', 'target': '3-抗非生物胁迫', 'value': 12.560408810016359, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-其他2', 'target': '3-种子处理', 'value': 17.667101231440025, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '2-其他2', 'target': '3-生物活性成分', 'value': 6.585368716093608, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-其他2', 'target': '3-病毒与昆虫生态', 'value': 16.263592323502937, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-其他2', 'target': '3-生物修复', 'value': 11.377447234765384, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-其他2', 'target': '3-菌根共生机制研究', 'value': 1.9993199731593474, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-其他2', 'target': '3-青贮发酵及饲料品质', 'value': 16.489234877549332, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-其他2', 'target': '3-遗传多样性研究', 'value': 20.11604105846514, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '2-其他2', 'target': '3-饲养价值', 'value': 7.657080597740964, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-其他2', 'target': '3-田间生产', 'value': 25.82115117115067, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '2-其他2', 'target': '3-抗非生物胁迫', 'value': 17.023662816132582, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '2-生长发育与生物合成调控', 'target': '3-种子处理', 'value': 9.108428820092017, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-生长发育与生物合成调控', 'target': '3-生物活性成分', 'value': 8.667049181731453, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-生长发育与生物合成调控', 'target': '3-病毒与昆虫生态', 'value': 16.389906159247197, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-生长发育与生物合成调控', 'target': '3-生物修复', 'value': 5.883969044362244, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-生长发育与生物合成调控', 'target': '3-菌根共生机制研究', 'value': 119.43973463696092, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '2-生长发育与生物合成调控', 'target': '3-青贮发酵及饲料品质', 'value': 9.486955780674975, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-生长发育与生物合成调控', 'target': '3-遗传多样性研究', 'value': 23.786903115901087, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-生长发育与生物合成调控', 'target': '3-饲养价值', 'value': 5.24725543936518, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-生长发育与生物合成调控', 'target': '3-田间生产', 'value': 5.306257653334967, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-生长发育与生物合成调控', 'target': '3-抗非生物胁迫', 'value': 42.68354016832993, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '2-种子处理', 'target': '3-种子处理', 'value': 28.97757726094021, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '2-种子处理', 'target': '3-生物活性成分', 'value': 7.389785264002699, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-种子处理', 'target': '3-病毒与昆虫生态', 'value': 17.266784055551177, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-种子处理', 'target': '3-生物修复', 'value': 13.64114046752461, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-种子处理', 'target': '3-菌根共生机制研究', 'value': 3.729588780615047, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-种子处理', 'target': '3-青贮发酵及饲料品质', 'value': 30.056242720655515, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '2-种子处理', 'target': '3-遗传多样性研究', 'value': 12.063951083199132, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-种子处理', 'target': '3-饲养价值', 'value': 9.4883844886336, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-种子处理', 'target': '3-田间生产', 'value': 22.048459120545548, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '2-种子处理', 'target': '3-抗非生物胁迫', 'value': 17.33808675833248, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-菌根共生机制研究', 'target': '3-种子处理', 'value': 7.131633476677254, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-菌根共生机制研究', 'target': '3-生物活性成分', 'value': 9.90664586274734, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-菌根共生机制研究', 'target': '3-病毒与昆虫生态', 'value': 10.091085002412976, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-菌根共生机制研究', 'target': '3-生物修复', 'value': 37.552017516370526, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '2-菌根共生机制研究', 'target': '3-菌根共生机制研究', 'value': 77.77458133528617, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '2-菌根共生机制研究', 'target': '3-青贮发酵及饲料品质', 'value': 9.593068106433295, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-菌根共生机制研究', 'target': '3-遗传多样性研究', 'value': 7.387677405282318, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-菌根共生机制研究', 'target': '3-饲养价值', 'value': 3.6408719696521077, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-菌根共生机制研究', 'target': '3-田间生产', 'value': 10.61368731512471, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-菌根共生机制研究', 'target': '3-抗非生物胁迫', 'value': 15.308732010013303, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-遗传多样性研究', 'target': '3-种子处理', 'value': 11.968696867293092, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-遗传多样性研究', 'target': '3-生物活性成分', 'value': 8.291012783016301, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-遗传多样性研究', 'target': '3-病毒与昆虫生态', 'value': 29.657537801581952, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '2-遗传多样性研究', 'target': '3-生物修复', 'value': 12.126494637897693, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-遗传多样性研究', 'target': '3-菌根共生机制研究', 'value': 16.521293458470183, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-遗传多样性研究', 'target': '3-青贮发酵及饲料品质', 'value': 12.980220088195004, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-遗传多样性研究', 'target': '3-遗传多样性研究', 'value': 37.885693655052414, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '2-遗传多样性研究', 'target': '3-饲养价值', 'value': 4.863429948960535, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-遗传多样性研究', 'target': '3-田间生产', 'value': 16.803385662552454, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-遗传多样性研究', 'target': '3-抗非生物胁迫', 'value': 15.902235096980368, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-昆虫生态', 'target': '3-种子处理', 'value': 9.397321996201539, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-昆虫生态', 'target': '3-生物活性成分', 'value': 6.721257510490792, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-昆虫生态', 'target': '3-病毒与昆虫生态', 'value': 24.599159271097623, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '2-昆虫生态', 'target': '3-生物修复', 'value': 9.01574387476123, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-昆虫生态', 'target': '3-菌根共生机制研究', 'value': 2.142379424834374, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-昆虫生态', 'target': '3-青贮发酵及饲料品质', 'value': 10.628160272858656, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-昆虫生态', 'target': '3-遗传多样性研究', 'value': 12.477812175325031, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '2-昆虫生态', 'target': '3-饲养价值', 'value': 4.177956874210419, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-昆虫生态', 'target': '3-田间生产', 'value': 14.046679131623094, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '2-昆虫生态', 'target': '3-抗非生物胁迫', 'value': 9.793529468597242, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-其他3', 'target': '3-种子处理', 'value': 15.485655058454093, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-其他3', 'target': '3-生物活性成分', 'value': 5.850759740932151, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-其他3', 'target': '3-病毒与昆虫生态', 'value': 15.923207235747538, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-其他3', 'target': '3-生物修复', 'value': 37.724864413159914, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '2-其他3', 'target': '3-菌根共生机制研究', 'value': 2.8435355144822214, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-其他3', 'target': '3-青贮发酵及饲料品质', 'value': 16.825401612965944, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-其他3', 'target': '3-遗传多样性研究', 'value': 11.549674550750312, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-其他3', 'target': '3-饲养价值', 'value': 7.829834466026031, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-其他3', 'target': '3-田间生产', 'value': 33.64911066753503, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '2-其他3', 'target': '3-抗非生物胁迫', 'value': 16.317956739946776, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-抗非生物胁迫', 'target': '3-种子处理', 'value': 20.653796885861674, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-抗非生物胁迫', 'target': '3-生物活性成分', 'value': 6.77029247995077, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-抗非生物胁迫', 'target': '3-病毒与昆虫生态', 'value': 19.804100989974746, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-抗非生物胁迫', 'target': '3-生物修复', 'value': 18.6295247295276, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-抗非生物胁迫', 'target': '3-菌根共生机制研究', 'value': 9.115322857549444, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-抗非生物胁迫', 'target': '3-青贮发酵及饲料品质', 'value': 18.871794235986343, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-抗非生物胁迫', 'target': '3-遗传多样性研究', 'value': 15.192347119484827, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-抗非生物胁迫', 'target': '3-饲养价值', 'value': 8.101224855923986, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-抗非生物胁迫', 'target': '3-田间生产', 'value': 25.78445231588425, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '2-抗非生物胁迫', 'target': '3-抗非生物胁迫', 'value': 56.077143529856336, 'lineStyle': {'color': 'source', 'opacity': 0.2}}]
    links = [{'source': '1-Growth and synthesis regulation', 'target': '2-Cannot name exactly1', 'value': 13.04289522595014, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Growth and synthesis regulation', 'target': '2-Feeding value', 'value': 5.347046091321203, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Growth and synthesis regulation', 'target': '2-Cannot name exactly2', 'value': 20.835293526583648, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '1-Growth and synthesis regulation', 'target': '2-Growth and synthesis regulation', 'value': 8.92791442932558, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Growth and synthesis regulation', 'target': '2-Seed treatment', 'value': 13.724875819428853, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Growth and synthesis regulation', 'target': '2-Mechanism of mycorrhizal symbiosis', 'value': 4.139875618764864, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Growth and synthesis regulation', 'target': '2-Genetic diversity research', 'value': 40.258863610408575, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '1-Growth and synthesis regulation', 'target': '2-Insect ecology', 'value': 18.359357701549442, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '1-Growth and synthesis regulation', 'target': '2-Cannot name exactly3', 'value': 11.607317979976028, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Growth and synthesis regulation', 'target': '2-Resistance to abiotic stress', 'value': 11.75655999669167, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Bioremediation', 'target': '2-Cannot name exactly1', 'value': 12.78817285181044, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Bioremediation', 'target': '2-Feeding value', 'value': 8.021376134925777, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Bioremediation', 'target': '2-Cannot name exactly2', 'value': 19.55267997528968, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '1-Bioremediation', 'target': '2-Growth and synthesis regulation', 'value': 2.2513313661549237, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Bioremediation', 'target': '2-Seed treatment', 'value': 23.69707125803412, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '1-Bioremediation', 'target': '2-Mechanism of mycorrhizal symbiosis', 'value': 4.748361976854138, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Bioremediation', 'target': '2-Genetic diversity research', 'value': 10.435172061055354, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Bioremediation', 'target': '2-Insect ecology', 'value': 12.157430926383686, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Bioremediation', 'target': '2-Cannot name exactly3', 'value': 22.09146524274016, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '1-Bioremediation', 'target': '2-Resistance to abiotic stress', 'value': 15.256938206751705, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Resistance to abiotic stress', 'target': '2-Cannot name exactly1', 'value': 10.853284563042335, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Resistance to abiotic stress', 'target': '2-Feeding value', 'value': 7.005959416450491, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Resistance to abiotic stress', 'target': '2-Cannot name exactly2', 'value': 19.067424643417112, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '1-Resistance to abiotic stress', 'target': '2-Growth and synthesis regulation', 'value': 4.7873377533123325, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Resistance to abiotic stress', 'target': '2-Seed treatment', 'value': 16.068109414186292, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Resistance to abiotic stress', 'target': '2-Mechanism of mycorrhizal symbiosis', 'value': 7.129483965959265, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Resistance to abiotic stress', 'target': '2-Genetic diversity research', 'value': 10.302642842221262, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Resistance to abiotic stress', 'target': '2-Insect ecology', 'value': 10.2087965306567, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Resistance to abiotic stress', 'target': '2-Cannot name exactly3', 'value': 16.174648046776838, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Resistance to abiotic stress', 'target': '2-Resistance to abiotic stress', 'value': 41.40231282397738, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '1-Feed nutrition', 'target': '2-Cannot name exactly1', 'value': 15.183714200306255, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '1-Feed nutrition', 'target': '2-Feeding value', 'value': 14.076670121098621, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Feed nutrition', 'target': '2-Cannot name exactly2', 'value': 19.71285699894183, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '1-Feed nutrition', 'target': '2-Growth and synthesis regulation', 'value': 2.665881883748569, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Feed nutrition', 'target': '2-Seed treatment', 'value': 20.329404069043395, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '1-Feed nutrition', 'target': '2-Mechanism of mycorrhizal symbiosis', 'value': 1.3997164120698031, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Feed nutrition', 'target': '2-Genetic diversity research', 'value': 9.603611348713256, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Feed nutrition', 'target': '2-Insect ecology', 'value': 10.468907683358792, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Feed nutrition', 'target': '2-Cannot name exactly3', 'value': 13.088546376097275, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Feed nutrition', 'target': '2-Resistance to abiotic stress', 'value': 11.470690906622211, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Feeding value', 'target': '2-Cannot name exactly1', 'value': 21.812307300151264, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '1-Feeding value', 'target': '2-Feeding value', 'value': 56.116820569159216, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '1-Feeding value', 'target': '2-Cannot name exactly2', 'value': 15.864790946051, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Feeding value', 'target': '2-Growth and synthesis regulation', 'value': 2.1125442951147817, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Feeding value', 'target': '2-Seed treatment', 'value': 22.64399521463607, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '1-Feeding value', 'target': '2-Mechanism of mycorrhizal symbiosis', 'value': 3.150606312076271, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Feeding value', 'target': '2-Genetic diversity research', 'value': 7.880126248903415, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Feeding value', 'target': '2-Insect ecology', 'value': 9.64018604600679, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Feeding value', 'target': '2-Cannot name exactly3', 'value': 13.428323767350351, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Feeding value', 'target': '2-Resistance to abiotic stress', 'value': 10.35029930055084, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Mechanism of mycorrhizal symbiosis', 'target': '2-Cannot name exactly1', 'value': 6.961692043997001, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Mechanism of mycorrhizal symbiosis', 'target': '2-Feeding value', 'value': 2.312039167831921, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Mechanism of mycorrhizal symbiosis', 'target': '2-Cannot name exactly2', 'value': 2.348599875212804, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Mechanism of mycorrhizal symbiosis', 'target': '2-Growth and synthesis regulation', 'value': 23.871681963364562, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '1-Mechanism of mycorrhizal symbiosis', 'target': '2-Seed treatment', 'value': 6.1622508633423, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Mechanism of mycorrhizal symbiosis', 'target': '2-Mechanism of mycorrhizal symbiosis', 'value': 85.11129516684034, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '1-Mechanism of mycorrhizal symbiosis', 'target': '2-Genetic diversity research', 'value': 10.466816574554901, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Mechanism of mycorrhizal symbiosis', 'target': '2-Insect ecology', 'value': 3.023547558360073, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Mechanism of mycorrhizal symbiosis', 'target': '2-Cannot name exactly3', 'value': 13.108715381451917, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Mechanism of mycorrhizal symbiosis', 'target': '2-Resistance to abiotic stress', 'value': 8.633361405044214, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Genetic diversity research', 'target': '2-Cannot name exactly1', 'value': 4.464158318142111, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Genetic diversity research', 'target': '2-Feeding value', 'value': 4.988804577529551, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Genetic diversity research', 'target': '2-Cannot name exactly2', 'value': 6.357586163583757, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Genetic diversity research', 'target': '2-Growth and synthesis regulation', 'value': 94.19277867851126, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '1-Genetic diversity research', 'target': '2-Seed treatment', 'value': 10.95735172490792, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Genetic diversity research', 'target': '2-Mechanism of mycorrhizal symbiosis', 'value': 28.36892071498293, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '1-Genetic diversity research', 'target': '2-Genetic diversity research', 'value': 35.346854397109574, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '1-Genetic diversity research', 'target': '2-Insect ecology', 'value': 4.830808235634747, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Genetic diversity research', 'target': '2-Cannot name exactly3', 'value': 3.744796968259628, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Genetic diversity research', 'target': '2-Resistance to abiotic stress', 'value': 18.747940221338528, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Cannot name exactly', 'target': '2-Cannot name exactly1', 'value': 40.698130381313135, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '1-Cannot name exactly', 'target': '2-Feeding value', 'value': 13.721287561384619, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Cannot name exactly', 'target': '2-Cannot name exactly2', 'value': 24.706009278140556, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '1-Cannot name exactly', 'target': '2-Growth and synthesis regulation', 'value': 2.3510245421930356, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Cannot name exactly', 'target': '2-Seed treatment', 'value': 16.72540665509428, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Cannot name exactly', 'target': '2-Mechanism of mycorrhizal symbiosis', 'value': 2.691266245653703, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Cannot name exactly', 'target': '2-Genetic diversity research', 'value': 11.734537917735466, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Cannot name exactly', 'target': '2-Insect ecology', 'value': 11.91077852658844, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Cannot name exactly', 'target': '2-Cannot name exactly3', 'value': 13.313383592100344, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Cannot name exactly', 'target': '2-Resistance to abiotic stress', 'value': 11.14817529979644, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Field production and environmental impact', 'target': '2-Cannot name exactly1', 'value': 19.57791225828202, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '1-Field production and environmental impact', 'target': '2-Feeding value', 'value': 9.33294103051548, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Field production and environmental impact', 'target': '2-Cannot name exactly2', 'value': 19.591491920924078, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '1-Field production and environmental impact', 'target': '2-Growth and synthesis regulation', 'value': 1.044729921900024, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Field production and environmental impact', 'target': '2-Seed treatment', 'value': 16.723783712887855, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Field production and environmental impact', 'target': '2-Mechanism of mycorrhizal symbiosis', 'value': 4.444497173227017, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Field production and environmental impact', 'target': '2-Genetic diversity research', 'value': 10.117647586687152, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Field production and environmental impact', 'target': '2-Insect ecology', 'value': 12.656776140252838, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Field production and environmental impact', 'target': '2-Cannot name exactly3', 'value': 33.77466507640923, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '1-Field production and environmental impact', 'target': '2-Resistance to abiotic stress', 'value': 12.735555178914307, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Insect ecology', 'target': '2-Cannot name exactly1', 'value': 11.842525414567758, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Insect ecology', 'target': '2-Feeding value', 'value': 5.399860128906238, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Insect ecology', 'target': '2-Cannot name exactly2', 'value': 16.695683749926726, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '1-Insect ecology', 'target': '2-Growth and synthesis regulation', 'value': 1.654434659091319, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Insect ecology', 'target': '2-Seed treatment', 'value': 12.580217579562186, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Insect ecology', 'target': '2-Mechanism of mycorrhizal symbiosis', 'value': 1.3824033311344828, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Insect ecology', 'target': '2-Genetic diversity research', 'value': 13.72224653723773, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '1-Insect ecology', 'target': '2-Insect ecology', 'value': 23.660447832610007, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '1-Insect ecology', 'target': '2-Cannot name exactly3', 'value': 10.815889711227046, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '1-Insect ecology', 'target': '2-Resistance to abiotic stress', 'value': 9.246291055736512, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Cannot name exactly1', 'target': '3-Seed treatment', 'value': 10.702257286669907, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Cannot name exactly1', 'target': '3-Biologically active ingredients', 'value': 29.906096882695312, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '2-Cannot name exactly1', 'target': '3-Virus and insect ecology', 'value': 15.276749223743607, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Cannot name exactly1', 'target': '3-Bioremediation', 'value': 12.115880162609837, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Cannot name exactly1', 'target': '3-Mechanism of mycorrhizal symbiosis', 'value': 2.786561477117648, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Cannot name exactly1', 'target': '3-Silage fermentation and feed quality', 'value': 16.081385781939105, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Cannot name exactly1', 'target': '3-Genetic diversity research', 'value': 11.846425798163374, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Cannot name exactly1', 'target': '3-Feeding value', 'value': 8.093214241441276, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Cannot name exactly1', 'target': '3-Field production', 'value': 24.51527827588873, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '2-Cannot name exactly1', 'target': '3-Resistance to abiotic stress', 'value': 11.67615086973122, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Feeding value', 'target': '3-Seed treatment', 'value': 13.734832212062349, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Feeding value', 'target': '3-Biologically active ingredients', 'value': 13.073499861073312, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Feeding value', 'target': '3-Virus and insect ecology', 'value': 11.420201114303302, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Feeding value', 'target': '3-Bioremediation', 'value': 10.464467615386665, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Feeding value', 'target': '3-Mechanism of mycorrhizal symbiosis', 'value': 2.3763027553501743, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Feeding value', 'target': '3-Silage fermentation and feed quality', 'value': 30.68474877577769, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '2-Feeding value', 'target': '3-Genetic diversity research', 'value': 9.079669512721598, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Feeding value', 'target': '3-Feeding value', 'value': 59.628186402781594, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '2-Feeding value', 'target': '3-Field production', 'value': 20.977682940526986, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Feeding value', 'target': '3-Resistance to abiotic stress', 'value': 12.560408810016359, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Cannot name exactly2', 'target': '3-Seed treatment', 'value': 17.667101231440025, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '2-Cannot name exactly2', 'target': '3-Biologically active ingredients', 'value': 6.585368716093608, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Cannot name exactly2', 'target': '3-Virus and insect ecology', 'value': 16.263592323502937, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Cannot name exactly2', 'target': '3-Bioremediation', 'value': 11.377447234765384, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Cannot name exactly2', 'target': '3-Mechanism of mycorrhizal symbiosis', 'value': 1.9993199731593474, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Cannot name exactly2', 'target': '3-Silage fermentation and feed quality', 'value': 16.489234877549332, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Cannot name exactly2', 'target': '3-Genetic diversity research', 'value': 20.11604105846514, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '2-Cannot name exactly2', 'target': '3-Feeding value', 'value': 7.657080597740964, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Cannot name exactly2', 'target': '3-Field production', 'value': 25.82115117115067, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '2-Cannot name exactly2', 'target': '3-Resistance to abiotic stress', 'value': 17.023662816132582, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '2-Growth and synthesis regulation', 'target': '3-Seed treatment', 'value': 9.108428820092017, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Growth and synthesis regulation', 'target': '3-Biologically active ingredients', 'value': 8.667049181731453, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Growth and synthesis regulation', 'target': '3-Virus and insect ecology', 'value': 16.389906159247197, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Growth and synthesis regulation', 'target': '3-Bioremediation', 'value': 5.883969044362244, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Growth and synthesis regulation', 'target': '3-Mechanism of mycorrhizal symbiosis', 'value': 119.43973463696092, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '2-Growth and synthesis regulation', 'target': '3-Silage fermentation and feed quality', 'value': 9.486955780674975, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Growth and synthesis regulation', 'target': '3-Genetic diversity research', 'value': 23.786903115901087, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Growth and synthesis regulation', 'target': '3-Feeding value', 'value': 5.24725543936518, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Growth and synthesis regulation', 'target': '3-Field production', 'value': 5.306257653334967, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Growth and synthesis regulation', 'target': '3-Resistance to abiotic stress', 'value': 42.68354016832993, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '2-Seed treatment', 'target': '3-Seed treatment', 'value': 28.97757726094021, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '2-Seed treatment', 'target': '3-Biologically active ingredients', 'value': 7.389785264002699, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Seed treatment', 'target': '3-Virus and insect ecology', 'value': 17.266784055551177, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Seed treatment', 'target': '3-Bioremediation', 'value': 13.64114046752461, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Seed treatment', 'target': '3-Mechanism of mycorrhizal symbiosis', 'value': 3.729588780615047, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Seed treatment', 'target': '3-Silage fermentation and feed quality', 'value': 30.056242720655515, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '2-Seed treatment', 'target': '3-Genetic diversity research', 'value': 12.063951083199132, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Seed treatment', 'target': '3-Feeding value', 'value': 9.4883844886336, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Seed treatment', 'target': '3-Field production', 'value': 22.048459120545548, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '2-Seed treatment', 'target': '3-Resistance to abiotic stress', 'value': 17.33808675833248, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Mechanism of mycorrhizal symbiosis', 'target': '3-Seed treatment', 'value': 7.131633476677254, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Mechanism of mycorrhizal symbiosis', 'target': '3-Biologically active ingredients', 'value': 9.90664586274734, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Mechanism of mycorrhizal symbiosis', 'target': '3-Virus and insect ecology', 'value': 10.091085002412976, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Mechanism of mycorrhizal symbiosis', 'target': '3-Bioremediation', 'value': 37.552017516370526, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '2-Mechanism of mycorrhizal symbiosis', 'target': '3-Mechanism of mycorrhizal symbiosis', 'value': 77.77458133528617, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '2-Mechanism of mycorrhizal symbiosis', 'target': '3-Silage fermentation and feed quality', 'value': 9.593068106433295, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Mechanism of mycorrhizal symbiosis', 'target': '3-Genetic diversity research', 'value': 7.387677405282318, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Mechanism of mycorrhizal symbiosis', 'target': '3-Feeding value', 'value': 3.6408719696521077, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Mechanism of mycorrhizal symbiosis', 'target': '3-Field production', 'value': 10.61368731512471, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Mechanism of mycorrhizal symbiosis', 'target': '3-Resistance to abiotic stress', 'value': 15.308732010013303, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Genetic diversity research', 'target': '3-Seed treatment', 'value': 11.968696867293092, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Genetic diversity research', 'target': '3-Biologically active ingredients', 'value': 8.291012783016301, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Genetic diversity research', 'target': '3-Virus and insect ecology', 'value': 29.657537801581952, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '2-Genetic diversity research', 'target': '3-Bioremediation', 'value': 12.126494637897693, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Genetic diversity research', 'target': '3-Mechanism of mycorrhizal symbiosis', 'value': 16.521293458470183, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Genetic diversity research', 'target': '3-Silage fermentation and feed quality', 'value': 12.980220088195004, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Genetic diversity research', 'target': '3-Genetic diversity research', 'value': 37.885693655052414, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '2-Genetic diversity research', 'target': '3-Feeding value', 'value': 4.863429948960535, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Genetic diversity research', 'target': '3-Field production', 'value': 16.803385662552454, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Genetic diversity research', 'target': '3-Resistance to abiotic stress', 'value': 15.902235096980368, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Insect ecology', 'target': '3-Seed treatment', 'value': 9.397321996201539, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Insect ecology', 'target': '3-Biologically active ingredients', 'value': 6.721257510490792, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Insect ecology', 'target': '3-Virus and insect ecology', 'value': 24.599159271097623, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '2-Insect ecology', 'target': '3-Bioremediation', 'value': 9.01574387476123, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Insect ecology', 'target': '3-Mechanism of mycorrhizal symbiosis', 'value': 2.142379424834374, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Insect ecology', 'target': '3-Silage fermentation and feed quality', 'value': 10.628160272858656, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Insect ecology', 'target': '3-Genetic diversity research', 'value': 12.477812175325031, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '2-Insect ecology', 'target': '3-Feeding value', 'value': 4.177956874210419, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Insect ecology', 'target': '3-Field production', 'value': 14.046679131623094, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '2-Insect ecology', 'target': '3-Resistance to abiotic stress', 'value': 9.793529468597242, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Cannot name exactly3', 'target': '3-Seed treatment', 'value': 15.485655058454093, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Cannot name exactly3', 'target': '3-Biologically active ingredients', 'value': 5.850759740932151, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Cannot name exactly3', 'target': '3-Virus and insect ecology', 'value': 15.923207235747538, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Cannot name exactly3', 'target': '3-Bioremediation', 'value': 37.724864413159914, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '2-Cannot name exactly3', 'target': '3-Mechanism of mycorrhizal symbiosis', 'value': 2.8435355144822214, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Cannot name exactly3', 'target': '3-Silage fermentation and feed quality', 'value': 16.825401612965944, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Cannot name exactly3', 'target': '3-Genetic diversity research', 'value': 11.549674550750312, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Cannot name exactly3', 'target': '3-Feeding value', 'value': 7.829834466026031, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Cannot name exactly3', 'target': '3-Field production', 'value': 33.64911066753503, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '2-Cannot name exactly3', 'target': '3-Resistance to abiotic stress', 'value': 16.317956739946776, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Resistance to abiotic stress', 'target': '3-Seed treatment', 'value': 20.653796885861674, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Resistance to abiotic stress', 'target': '3-Biologically active ingredients', 'value': 6.77029247995077, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Resistance to abiotic stress', 'target': '3-Virus and insect ecology', 'value': 19.804100989974746, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Resistance to abiotic stress', 'target': '3-Bioremediation', 'value': 18.6295247295276, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Resistance to abiotic stress', 'target': '3-Mechanism of mycorrhizal symbiosis', 'value': 9.115322857549444, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Resistance to abiotic stress', 'target': '3-Silage fermentation and feed quality', 'value': 18.871794235986343, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Resistance to abiotic stress', 'target': '3-Genetic diversity research', 'value': 15.192347119484827, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Resistance to abiotic stress', 'target': '3-Feeding value', 'value': 8.101224855923986, 'lineStyle': {'color': 'white', 'opacity': 0}}, {'source': '2-Resistance to abiotic stress', 'target': '3-Field production', 'value': 25.78445231588425, 'lineStyle': {'color': 'source', 'opacity': 0.2}}, {'source': '2-Resistance to abiotic stress', 'target': '3-Resistance to abiotic stress', 'value': 56.077143529856336, 'lineStyle': {'color': 'source', 'opacity': 0.2}}]


    c = (
        Sankey(init_opts=opts.InitOpts(width=" 1200px", height="800px"))
            .add(
            "sankey",
            nodes,
            links,
            linestyle_opt=opts.LineStyleOpts(curve=0.5),
            label_opts=opts.LabelOpts(position="right"),
        )
            .set_global_opts(title_opts=opts.TitleOpts(title="Sankey-基本示例"))
            .render(save_root + "10-主题演化图.html")
    )




# fawenliang_per_year()       # 2-每年发文量（单条折线）
# top_10_journal()            # 31-前10期刊每年发文量（柱状图）
# top_5_journal_per_year()    # 32-发文量前5期刊的每年发文量（多条折线图）
# country_all()               # 41-所有国家发文量，分档显示（地图）
# top_10_country()            # 42-发文量前十国家的发文量（柱状图）
# top_5_country()             # 43-前5国家每年发文量（河流图）
# top_5_country_line()        # 43-前5国家每年发文量（多条折线）
# top5_country_by_oneself()   # 44-前5国家独自与合作发文情况
# top_15_org()                # 51-发文量前15机构的发文量（柱状图）
# top_10_org_river()          # 52-发文前10机构每年发文量（河流图）
# top_5_org_line()            # 52-前5发文机构每年发文量（折线图）
# top_10_financial_bar()      # 61-资金来源前十（柱状图）
# top_10_financial_bar_horizontal()  # 61-资金来源前十（横着的柱状图）
# top_5_financial_time_line() # 62-资金前5每年资助论文数量（折线图）
# top_10_subject_scatter()    # 71-前10学科分布，柱状图
# top_10_country_subject()    # 72-前十国家的学科分布，雷达图，目前没有用
# Plant_Sciences()            # 72-Plant Sciences在前10国家中的占比情况
# interdisciplinary()         # 73-交叉学科（热力图）
# strategic_coordinates()     # 8-战略坐标
# topic_distribution()        # 9-主题分布图
topic_evolution()           # 10-主题演化图
