from src.data_analysis import analysis_trail
from src.data_analysis import analysis_together
path = 'D:/zyx-project/paper/python_paper/'
import pandas as pd


# ----------------------------------------------Registration platform analysis-----------------------
# # # Results of each registered platform
paper_number_excel = path + 'analysis_result/试验_注册平台_发文量.xlsx'
analysis_trail.get_source_number(paper_number_excel)

# # # Amount of papers issued by each registered platform Country
paper_number_excel = path + 'analysis_result/试验_注册平台_发文量.xlsx'
country_number_excel = path + 'analysis_result/国家_发文量_试验.xlsx'
paper_result_excel = path + 'analysis_result/试验_注册平台_发文量_按国家结果.xlsx'
analysis_trail.source_top10_country(paper_number_excel, country_number_excel, paper_result_excel)

# ----------------------------------------------Blind judgment analysis-----------------------
# retrieve data
trail_file_name = path + 'data_set/trail_1231_filter_blind_label.xlsx'
country_dict_name = path + "data_set/试验_当前所有国家.xlsx"
country_number_excel = path + 'analysis_result/国家_发文量_试验.xlsx'

data_result_file = path + 'data_set/trail_1231_filter_blind_label_tongji.xlsx'
result_file_with_number = path + 'analysis_result/trail_table_with_number.xlsx'
result_file = path + 'analysis_result/trail_table.xlsx'
# # Dictionary
phase_dict_file = path + "data_set/trail_indictor_dict/phase_dict.xlsx"
phase_result_file = path + "data_set/trail_indictor_dict/phase_result.xlsx"
size_dict_file = path + "data_set/trail_indictor_dict/size_dict.xlsx"
size_result_file = path + "data_set/trail_indictor_dict/size_result.xlsx"
gender_dict_file = path + "data_set/trail_indictor_dict/gender_dict.xlsx"
gender_result_file = path + "data_set/trail_indictor_dict/gender_result.xlsx"
age_dict_file = path + "data_set/trail_indictor_dict/age_dict.xlsx"
#
analysis_trail.get_blind_table(trail_file_name, country_dict_name, country_number_excel, phase_dict_file, phase_result_file,
                               size_dict_file, size_result_file, gender_dict_file, gender_result_file, age_dict_file,
                               data_result_file, result_file_with_number, result_file)
to_file = path + 'analysis_result/trail_radio_table.xlsx'
analysis_trail.get_blind_radio_table(result_file, to_file)
