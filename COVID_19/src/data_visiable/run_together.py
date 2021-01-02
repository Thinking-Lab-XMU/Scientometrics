from src.data_visiable import visiable_together

path = 'D:/zyx-project/paper/python_paper/'
month_number = 12
# #
# #
# # # ----------------------------------------------总体情况-----------------------
# # TODO: Together with the growth rate of the number of infections, line
# data_file_name = path + 'analysis_result/每月成果数.xlsx'
# to_file_name = path + 'visiable_result/month_number_people_rate.html'
# svg_name = path + 'visiable_result/month_number_people_rate.svg'
# visiable_together.draw_over_all_with_radio(data_file_name, to_file_name, svg_name)
# print('---The overall analysis is complete！')
# #
# # # ----------------------------------------------Country situation-----------------------
# # TODO：The total amount of papers, trials, and publications in each country
# dict_file = path + 'analysis_result/echarts和covid映射.xlsx'
# number_excel = path + 'analysis_result/国家_发文量_论文.xlsx'
# to_file = path + 'visiable_result/together-country-count-paper-geo.html'
# svg_name = path + 'visiable_result/together-country-count-paper-geo.svg'
# label_name = 'No. of papers'
# visiable_together.draw_country_number(dict_file, number_excel, to_file, svg_name, label_name)
#
# dict_file = path + 'analysis_result/echarts和covid映射.xlsx'
# number_excel = path + 'analysis_result/国家_发文量_试验.xlsx'
# to_file = path + 'visiable_result/together-country-count-trail-geo.html'
# svg_name = path + 'visiable_result/together-country-count-trail-geo.svg'
# label_name = 'No. of trials'
# visiable_together.draw_country_number(dict_file, number_excel, to_file, svg_name, label_name)
# # #
# dict_file = path + 'analysis_result/echarts和covid映射.xlsx'
# number_excel = path + 'analysis_result/国家_发文量_一起.xlsx'
# to_file = path + 'visiable_result/together-country-count-together-geo.html'
# svg_name = path + 'visiable_result/together-country-count-together-geo.svg'
# label_name = 'No. of achievements'
# visiable_together.draw_country_number(dict_file, number_excel, to_file, svg_name, label_name)
#
# # ----top10 country ranking
# # Parallel coordinate
# data_file_name = path + 'analysis_result/国家_top10_列表.xlsx'
# to_file = path + 'visiable_result/together-country-top10_rank.html'
# svg_name = path + 'visiable_result/together-country-top10_rank.eps'
# visiable_together.draw_country_rank_change(data_file_name, to_file, svg_name)
# # # ----Top 10 countries posted monthly volume
# # # --Theme River
# # paper
# data_file_name = path + 'analysis_result/国家_一起top10_论文_按月结果.xlsx'
# to_file = path + 'visiable_result/country-together_top10-paper-monthly-themeriver.html'
# svg_name = path + 'visiable_result/country-together_top10-paper-monthly-themeriver.eps'
# stack = True
# y_name = 'No. of papers'
# visiable_together.draw_indicator_month_river(data_file_name, to_file, svg_name, month_number)
# # # # # # trial
# data_file_name = path + 'analysis_result/国家_一起top10_试验_按月结果.xlsx'
# to_file = path + 'visiable_result/country-together_top10-trial-monthly-themeriver.html'
# svg_name = path + 'visiable_result/country-together_top10-trial-monthly-themeriver.eps'
# stack = True
# y_name = 'No. of trials'
# visiable_together.draw_indicator_month_river(data_file_name, to_file, svg_name, month_number)
# # # # # # together
# data_file_name = path + 'analysis_result/国家_一起top10_一起_按月结果.xlsx'
# to_file = path + 'visiable_result/country-together_top10-together-monthly-themeriver.html'
# svg_name = path + 'visiable_result/country-together_top10-together-monthly-themeriver.eps'
# stack = True
# y_name = 'No. of achievements'
# visiable_together.draw_indicator_month_river(data_file_name, to_file, svg_name, month_number)

# # # # ----------------------------------------------Intervention methods-----------------------
# # # ----The amount of papers, experiments, and the total number of papers issued by each intervention
# # --Histogram-not stacked-not transposed
# data_file_name = path + 'analysis_result/介入手段_总体情况.xlsx'
# to_file = path + 'visiable_result/intervention-overall-bar.html'
# svg_name = path + 'visiable_result/intervention-overall-bar.eps'
# y_name = 'No.'
# stack = False
# reverse = True
# y_list = ['paper', 'trial']
# visiable_together.draw_overall_type_bar(data_file_name, to_file, svg_name, stack, y_name, y_list, reverse)

# # ----The amount of papers, trials, and monthly publications for each intervention
# # --line chart--
# # paper
# data_file_name = path + 'analysis_result/介入手段_发文量_论文_按月结果.xlsx'
# to_file = path + 'visiable_result/intervention-number-paper-monthly-line.html'
# svg_name = path + 'visiable_result/intervention-number-paper-monthly-line.eps'
# stack = False
# y_name = 'No. of papers'
# visiable_together.draw_indicator_month_link(data_file_name, to_file, svg_name, stack, month_number, y_name)
# # # # trial
# data_file_name = path + 'analysis_result/介入手段_发文量_试验_按月结果.xlsx'
# to_file = path + 'visiable_result/intervention-number-trial-monthly-line.html'
# svg_name = path + 'visiable_result/intervention-number-trial-monthly-line.eps'
# stack = False
# y_name = 'No. of trials'
# visiable_together.draw_indicator_month_link(data_file_name, to_file, svg_name, stack, month_number, y_name)
# # # together
# data_file_name = path + 'analysis_result/介入手段_发文量_一起_按月结果.xlsx'
# to_file = path + 'visiable_result/intervention-number-together-monthly-line.html'
# svg_name = path + 'visiable_result/intervention-number-together-monthly-line.eps'
# stack = False
# y_name = '               No. of achievements'
# visiable_together.draw_indicator_month_link(data_file_name, to_file, svg_name, stack, month_number, y_name)
# ----The amount of papers, trials, and top 10 countries for each intervention
# --scatter--
# # # paper
# data_file_name = path + 'analysis_result/介入手段_一起top10_论文_按国家结果.xlsx'
# svg_name = path + '/visiable_result/intervention-number-paper-country-scatter.html'
# size = 4
# y_name = 'No. of papers'
# visiable_together.draw_indicator_country_scatter(data_file_name, svg_name, size, y_name)
# # # # trial
# data_file_name = path + 'analysis_result/介入手段_一起top10_试验_按国家结果.xlsx'
# svg_name = path + 'visiable_result/intervention-number-trial-country-scatter.html'
# size = 4
# y_name = 'No. of trials'
# visiable_together.draw_indicator_country_scatter(data_file_name, svg_name, size, y_name)
# # # together
# data_file_name = path + 'analysis_result/介入手段_一起top10_一起_按国家结果.xlsx'
# svg_name = path + 'visiable_result/intervention-number-together-country-scatter.html'
# size = 4
# y_name = 'No. of achievements'
# visiable_together.draw_indicator_country_scatter(data_file_name, svg_name, size, y_name)
#
# # # ----------------------------------------------lda clustering situation-----------------------
# # # ----Each lda clustering papers, experiments, total number of papers
# # # --bar
data_file_name = path + 'analysis_result/层次聚类_总体情况.xlsx'
to_file = path + 'visiable_result/cluster-overall-bar.html'
svg_name = path + 'visiable_result/cluster-overall-bar.eps'
y_name = 'number'
stack = False
reverse = True
y_list = ['paper', 'trial']
visiable_together.draw_overall_type_bar(data_file_name, to_file, svg_name, stack, y_name, y_list, reverse, False)
# # ----Clustering papers, experiments, and monthly publication volume at each level
# # --Theme River--
# # paper
data_file_name = path + 'analysis_result/层次聚类_发文量_论文_按月结果.xlsx'
to_file = path + 'visiable_result/cluster-number-paper-monthly-themeriver.html'
svg_name = path + 'visiable_result/cluster-number-paper-monthly-themeriver.eps'
stack = True
y_name = 'No. of papers'
visiable_together.draw_indicator_month_river(data_file_name, to_file, svg_name, month_number, False)
# # trial
data_file_name = path + 'analysis_result/层次聚类_发文量_试验_按月结果.xlsx'
to_file = path + 'visiable_result/cluster-number-trial-monthly-themeriver.html'
svg_name = path + 'visiable_result/cluster-number-trial-monthly-themeriver.eps'
stack = True
y_name = 'No. of trials'
visiable_together.draw_indicator_month_river(data_file_name, to_file, svg_name, month_number, False)
# # together
data_file_name = path + 'analysis_result/层次聚类_发文量_一起_按月结果.xlsx'
to_file = path + 'visiable_result/cluster-number-together-monthly-themeriver.html'
svg_name = path + 'visiable_result/cluster-number-together-monthly-themeriver.eps'
stack = True
y_name = 'No. of achievements'
visiable_together.draw_indicator_month_river(data_file_name, to_file, svg_name, month_number, False)

# # # --散点图--
# # # 论文
data_file_name = path + 'analysis_result/层次聚类_一起top10_论文_按国家结果.xlsx'
svg_name = path + 'visiable_result/cluster-together_top10-paper-country-scatter.html'
size = 5
y_name = 'No. of papers'
visiable_together.draw_indicator_country_scatter(data_file_name, svg_name, size, y_name, False)
# # 试验
data_file_name = path + 'analysis_result/层次聚类_一起top10_试验_按国家结果.xlsx'
svg_name = path + 'visiable_result/cluster-together_top10-trial-country-scatter.html'
size = 5
y_name = 'No. of trails'
visiable_together.draw_indicator_country_scatter(data_file_name, svg_name, size, y_name, False)
# 一起
data_file_name = path + 'analysis_result/层次聚类_一起top10_一起_按国家结果.xlsx'
svg_name = path + 'visiable_result/cluster-together_top10-together-country-scatter.html'
size = 5
y_name = 'No. of achievements'
visiable_together.draw_indicator_country_scatter(data_file_name, svg_name, size, y_name, False)
# #