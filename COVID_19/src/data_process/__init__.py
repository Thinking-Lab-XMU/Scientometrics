"""
下载后主流程（注意中间信息的输出）：
1. 【论文】论文根据介入手段进行分类和筛选，并按照筛选结果获取新的txt
    a. 【论文】wos数据合并成一个excel, 按照时间（EA,PD）排序（nan放后面）,按照UT去重, 按照TI和AB去重, 表格增加月份字段
    b. 【论文】数据和关键词匹配，获得临床论文的excel（介入手段筛选）
    c. 【论文】按照UT,检索新的论文，生成新的txt（需要人工下载）
2. 【试验】
    a. 【试验】试验筛选（去掉非介入性等等）
    b. 【试验】介入手段筛选
    c. 【试验】进行盲法匹配（匹配完要人工看一下）
3. 【一起】
    a. 【一起】进行层次聚类，获得结果
    b. 【论文】拆分国家，机构，作者，资助机构等等（人工入库）
    c. 【试验】拆分拆分国家，作者到表格（人工入库）
The main process after downloading (note the output of intermediate information):
1. [Paper] Papers are classified and screened according to intervention methods, and new txt is obtained according to the screening results
     a. [Thesis] wos data is merged into one excel, sorted by time (EA, PD) (nan put after), deduplicated by UT, deduplicated by TI and AB, and added month field to the table
     b. [Paper] Data and keywords are matched to obtain excel for clinical papers (screening by interventional means)
     c. [Paper] According to UT, search for new papers and generate new txt (need to be downloaded manually)
2. [Test]
     a. [Experiment] Experimental screening (remove non-invasiveness, etc.)
     b. [Experiment] Screening of interventional means
     c. [Experiment] Perform blind matching (please check manually after matching)
3. [Together]
     a. [Together] Perform hierarchical clustering and obtain results
     b. [Paper] Split country, institution, author, funding institution, etc. (manual storage)
     c. [Experiment] Split country, author to table (manual storage)
"""
from src.data_process import paper_filter
from src.data_process import trial_filter
from src.data_process import lda

path = 'D:/zyx-project/paper/python_paper/'
# # --------------------论文筛选（paper filter）-------------------
# The first wave synthesizes excel, removes duplication, and adds month breakdown
# load_path = path + "data_set/paper_1231/"  # txt数据存储的根目录
# save_file = path + "data_set/paper_1231_drop_duplicates.xlsx"
# paper_filter.get_paper_excel(load_path, save_file)  # 生成excel
# print("--------End of the paper de-duplication, generate excel file--------")

# # # Judgment and screening of intervention methods
# data_path = path + "data_set/paper_1231_drop_duplicates.xlsx"
# temp_data_path = path + "data_set/paper_1231_drop_duplicates_filter_result.xlsx"
# filter_data_path = path + "data_set/paper_1231_filter.xlsx"
# dict_file_name = path + "data_set/201104-临床关键词(论文、试验通用）.xlsx"
# paper_filter.get_type(data_path, temp_data_path, filter_data_path, dict_file_name)
# #
# # # Generate new search fields for UT (if needed)
# # excel_file_name = path + "data_set/paper_1012_filter.xlsx"
# # paper_filter.get_ut_list(excel_file_name)
# #
# # # ---------------------trial filter-------------------
# De-duplication, de-cancelled trials, de-non-intrusive
# trail_file_name = path + 'data_set/trail_1231.xlsx'
# cancel_file_name = path + 'data_set/trail_1231_cancel.xlsx'
# drop_file_name = path + 'data_set/trail_1231_simple_filter.xlsx'
# duplicates_file = path + 'data_set/trail_1231_simple_filter_duplicates.xlsx'
# trial_filter.trial_excel(trail_file_name, cancel_file_name, drop_file_name, duplicates_file)
# #
# # trials data intervention method processing
# input_file_name = path + "data_set/trail_1231_simple_filter.xlsx"
# temp_file_name = path + "data_set/trail_1231_simple_filter_filter_result.xlsx"
# filter_data_path = path + "data_set/trail_1231_filter.xlsx"
# dict_file_name = path + "data_set/201104-临床关键词(论文、试验通用）.xlsx"
# trial_filter.get_type(dict_file_name, input_file_name, temp_file_name, filter_data_path)
# #
# # # Blind judgment of trial data (based on the previous results first, then according to the rules)
# data_file = path + "data_set/trail_1231_filter.xlsx"
# result_file = path + "data_set/trail_1231_filter_blind.xlsx"
# suiji_dict = path + "data_set/盲法判断/COVID19-web-result-随机字典.xlsx"
# duizhao_dict = path + "data_set/盲法判断/COVID19-web-result-对照字典.xlsx"
# mangfa_dict = path + "data_set/盲法判断/COVID19-web-result-盲法字典.xlsx"
# to_suiji_file = path + "data_set/盲法判断/随机匹配失败.xlsx"
# to_duizhao_file = path + "data_set/盲法判断/对照匹配失败.xlsx"
# to_mangfa_file = path + "data_set/盲法判断/盲法匹配失败.xlsx"
# trial_filter.get_blind_result(data_file, suiji_dict, to_suiji_file, duizhao_dict, to_duizhao_file, mangfa_dict,
#                               to_mangfa_file, result_file)

# # # ---------------------Clustering-------------------
# # # # TODO: Get corpus
mesh_file = path + "data_set/MESH主题词.xlsx"
dict_file_name = path + "data_set/201104-临床关键词(论文、试验通用）.xlsx"
synonyms_file = path + "data_set/synonyms.xlsx"
paper_file_name = path + "data_set/paper_1231_filter.xlsx"
trial_file_name = path + "data_set/trail_1231_filter_blind.xlsx"
context_file = path + "data_set/层次聚类语料.xlsx"
context_word_count = path + "data_set/层次聚类语料_词频.xlsx"
# lda.get_corpus_keyword_2(mesh_file, dict_file_name, synonyms_file, paper_file_name, trial_file_name, context_file,
#                          context_word_count)

# TODO: lda clustering
# topic_number = 7
# result_paper_file = path + "data_set/paper_1231_filter_label.xlsx"
# result_trail_file = path + "data_set/trail_1231_filter_blind_label.xlsx"
# label_word_file = path + "data_set/lda类别主要词.xlsx"
# result_topic_file = path + "data_set/lda聚类_所有词_分类详细结果_7.xlsx"
# most_relevant_file = path + "data_set/lda聚类_所有词_最相关文档_7.xlsx"
# html_file = 'lda_所有词_7.html'
# lda.get_result_lda(context_file, paper_file_name, trial_file_name, result_paper_file,
#                    result_trail_file, label_word_file, result_topic_file, most_relevant_file, topic_number, html_file)

# # TODO: Paper data split
wos_file_name = path + "data_set/paper_1231_filter_label.xlsx"
country_dict_name = path + "data_set/国家同义词表.xlsx"
org_dict_name = path + "data_set/200809-机构同义词.xlsx"
financial_dict_name = path + "data_set/论文_资助机构同义词表.xlsx"
paper_filter.get_excel_table(path, wos_file_name, country_dict_name, org_dict_name, financial_dict_name)
#
# TODO: trial data split
trail_file_name = path + "data_set/trail_1231_filter_blind_label.xlsx"
country_dict_name = path + "data_set/试验_当前所有国家.xlsx"
trial_filter.get_trail_table(path, trail_file_name, country_dict_name)
