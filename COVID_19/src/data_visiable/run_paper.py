from src.data_visiable import visiable_paper
from src.data_visiable import visiable_together

path = 'D:/zyx-project/paper/python_paper/'
month_number = 12
# ----------------------------------------------organization-----------------------
# ----Top10 organizations publish monthly volume
# --Scatter plot--
# paper
data_file_name = path + 'analysis_result/论文_机构_论文top10_论文_按月结果.xlsx'
svg_name = path + 'visiable_result/paper-org-paper_top10-paper-month-scatter.html'
size = 10
y_name = 'No. of papers'
visiable_together.draw_indicator_month_scatter(data_file_name, svg_name, month_number, size, y_name)

# # ----Top10 Institutional Intervention Methods
# --Scatter--
data_file_name = path + 'analysis_result/论文_机构_论文top10_论文_介入手段.xlsx'
svg_name = path + 'visiable_result/paper-org-paper_top10-paper-intervention-scatter.html'
size = 10
y_name = 'No. of papers'
visiable_paper.draw_indicator_country_scatter(data_file_name, svg_name, size, y_name)
#
# ----Top10 institutional hierarchical clustering situation
# # --Scatter--
data_file_name = path + 'analysis_result/论文_机构_论文top10_论文_层次聚类.xlsx'
svg_name = path + 'visiable_result/paper-org-paper_top10-paper-cluster-scatter.html'
size = 10
y_name = 'No. of papers'
visiable_paper.draw_indicator_country_scatter(data_file_name, svg_name, size, y_name, False)


# # ----------------------------------------------Journal analysis-----------------------
# Top10 post volume bar
paper_result_excel = path + 'analysis_result/论文_期刊_发文量_论文.xlsx'
y_list = ['SO', 'number']
to_file_name = path + 'visiable_result/paper-journal-number-paper-bar.html'
svg_file_name = path + 'visiable_result/paper-journal-number-paper-bar.eps'
y_name = 'No. of papers'
pos_left = '40%'
visiable_paper.draw_indicator_top10(paper_result_excel, y_list, to_file_name, svg_file_name, y_name, pos_left)
#
# ----Top10 journals monthly publication volume
# # # --Theme River Diagram--
data_file_name = path + 'analysis_result/论文_期刊_论文top10_论文_按月结果.xlsx'
to_file = path + 'visiable_result/paper-journal-paper_top10-monthly-river.html'
svg_name = path + 'visiable_result/paper-journal-paper_top10-monthly-river.eps'
stack = True
y_name = 'No. of papers'
pos_right = '59%'
width = '1600px'
visiable_paper.draw_indicator_month_river(data_file_name, to_file, svg_name, month_number, pos_right, width)

# # ----------------------------------------------Subject analysis-----------------------
# # ----Top10 post volume bar
paper_result_excel = path + 'analysis_result/论文_学科_发文量_论文.xlsx'
y_list = ['WC', 'number']
to_file_name = path + 'visiable_result/paper-subject-number-paper-bar.html'
svg_file_name = path + 'visiable_result/paper-subject-number-paper-bar.eps'
y_name = 'No. of papers'
pos_left = '25%'
visiable_paper.draw_indicator_top10(paper_result_excel, y_list, to_file_name, svg_file_name, y_name, pos_left)
#
# ----Top10 subject monthly publication volume
# --Scatter--
data_file_name = path + 'analysis_result/论文_学科_论文top10_论文_按月结果.xlsx'
svg_name = path + 'visiable_result/paper-subject-paper_top10-monthly-scatter.html'
size = 6
y_name = 'No. of papers'
visiable_together.draw_indicator_month_scatter(data_file_name, svg_name, month_number, size, y_name, False)

# # ----Top10 Disciplinary Countries
# --Scatter--
data_file_name = path + 'analysis_result/论文_学科_top10_论文_按国家结果.xlsx'
svg_name = path + 'visiable_result/paper-subject-paper_top10-country-scatter.html'
size = 6
y_name = 'No. of papers'
visiable_paper.draw_indicator_country_subject_scatter(data_file_name, svg_name, size, y_name)


