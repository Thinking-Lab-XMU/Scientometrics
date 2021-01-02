from src.data_visiable import visiable_paper
from src.data_visiable import visiable_together
from src.data_visiable import visiable_trial

path = 'D:/zyx-project/paper/python_paper/'
month_number = 10
# ----------------------------------------------Registration platform-----------------------
# --top10 registration platform
# # bar
# data_file_name = path + 'analysis_result/试验_注册平台_发文量.xlsx'
# to_file = path + 'visiable_result/trail-platform-number-pie.html'
# svg_name = path + 'visiable_result/trail-platform-number-pie.eps'
# y_list = ['number']
# visiable_trial.draw_overall_type_pie(data_file_name, to_file, svg_name, y_list)
#
# # ----Top10 national registration platform posting volume
# # --scatter--
# data_file_name = path + 'analysis_result/试验_注册平台_发文量_按国家结果.xlsx'
# svg_name = path + 'visiable_result/trail-platform-number-country-scatter.html'
# size = 5
# y_name = 'No. of trials'
# visiable_paper.draw_indicator_country_subject_scatter(data_file_name, svg_name, size, y_name)

# # ----Big statistics for trial
data_file_name = path + 'analysis_result/trail_table_with_number.xlsx'
svg_name = path + 'visiable_result/table-trail-heatmap.eps'
to_file = path + 'visiable_result/table-trail-heatmap.html'
visiable_trial.draw_heat_map_grid(data_file_name, to_file, svg_name)
