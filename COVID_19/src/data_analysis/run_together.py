from src.data_analysis import analysis_together

path = 'D:/zyx-project/paper/python_paper/'

print('Analyze the content together-------------------------------------------------------------------------------------')
# ----------------------------------------------总体情况-----------------------
patient_data_file = path + 'analysis_result/每月新增患者.xlsx'
to_file_name = path + 'analysis_result/每月成果数.xlsx'
analysis_together.get_over_all(patient_data_file, to_file_name)
# print('---The overall analysis is complete！')
# ----------------------------------------------国家情况-----------------------
# The total amount of papers, trials, and publications in each country
paper_number_excel = path + 'analysis_result/国家_发文量_论文.xlsx'
trail_number_excel = path + 'analysis_result/国家_发文量_试验.xlsx'
all_number_excel = path + 'analysis_result/国家_发文量_一起.xlsx'
analysis_together.get_country_number(paper_number_excel, trail_number_excel, all_number_excel)

# # Country-top10 analysis (paper, trials, together)
paper_number_excel = path + 'analysis_result/国家_发文量_论文.xlsx'
trail_number_excel = path + 'analysis_result/国家_发文量_试验.xlsx'
all_number_excel = path + 'analysis_result/国家_发文量_一起.xlsx'
paper_result_excel = path + 'analysis_result/国家_论文top10_论文.xlsx'
trail_result_excel = path + 'analysis_result/国家_试验top10_试验.xlsx'
all_result_excel = path + 'analysis_result/国家_一起top10_一起.xlsx'
paper_top10_excel = path + 'analysis_result/国家_一起top10_论文.xlsx'
trail_top10_excel = path + 'analysis_result/国家_一起top10_试验.xlsx'
analysis_together.get_country_top(paper_number_excel, trail_number_excel, all_number_excel, paper_result_excel,
                                  trail_result_excel, all_result_excel, paper_top10_excel, trail_top10_excel)
#
# # Put the top 10 together to prepare for parallel coordinates
paper_number_excel = path + 'analysis_result/国家_发文量_论文.xlsx'
trail_number_excel = path + 'analysis_result/国家_发文量_试验.xlsx'
all_number_excel = path + 'analysis_result/国家_发文量_一起.xlsx'
to_file = path + 'analysis_result/国家_top10_列表.xlsx'
analysis_together.country_top10_together(paper_number_excel, trail_number_excel, all_number_excel, to_file)

# # National monthly publication volume (papers, trials, total)
paper_number_excel = path + 'analysis_result/国家_发文量_论文.xlsx'
trail_number_excel = path + 'analysis_result/国家_发文量_试验.xlsx'
all_number_excel = path + 'analysis_result/国家_发文量_一起.xlsx'
paper_result_excel = path + 'analysis_result/国家_论文top10_论文_按月结果.xlsx'
trial_result_excel = path + 'analysis_result/国家_试验top10_试验_按月结果.xlsx'
all_result_excel = path + 'analysis_result/国家_一起top10_一起_按月结果.xlsx'
paper_top10_excel = path + 'analysis_result/国家_一起top10_论文_按月结果.xlsx'
trail_top10_excel = path + 'analysis_result/国家_一起top10_试验_按月结果.xlsx'
analysis_together.country_top10_month(paper_number_excel, trail_number_excel, all_number_excel, paper_result_excel,
                                      trial_result_excel, all_result_excel, paper_top10_excel, trail_top10_excel)
print('---Country analysis completed！')

# # # ----------------------------------------------Intervention methods-----------------------
# Overall situation
to_file = path + 'analysis_result/介入手段_总体情况.xlsx'
label = 'topic'
analysis_together.get_intervention_number(to_file, label)
# # Month situation
paper_result_excel = path + 'analysis_result/介入手段_发文量_论文_按月结果.xlsx'
trial_result_excel = path + 'analysis_result/介入手段_发文量_试验_按月结果.xlsx'
all_result_excel = path + 'analysis_result/介入手段_发文量_一起_按月结果.xlsx'
label_file = path + 'analysis_result/介入手段_总体情况.xlsx'
label = 'topic'
analysis_together.get_intervention_month(paper_result_excel, trial_result_excel, all_result_excel, label, label_file)
# # Country situation
paper_number_excel = path + 'analysis_result/国家_发文量_论文.xlsx'
trail_number_excel = path + 'analysis_result/国家_发文量_试验.xlsx'
all_number_excel = path + 'analysis_result/国家_发文量_一起.xlsx'
paper_result_excel = path + 'analysis_result/介入手段_论文top10_论文_按国家结果.xlsx'
trial_result_excel = path + 'analysis_result/介入手段_试验top10_试验_按国家结果.xlsx'
all_result_excel = path + 'analysis_result/介入手段_一起top10_一起_按国家结果.xlsx'
paper_top10_excel = path + 'analysis_result/介入手段_一起top10_论文_按国家结果.xlsx'
trial_top10_excel = path + 'analysis_result/介入手段_一起top10_试验_按国家结果.xlsx'
label = 'topic'
analysis_together.country_top10_intervention(paper_number_excel, trail_number_excel, all_number_excel, paper_result_excel,
                        trial_result_excel, all_result_excel, paper_top10_excel, trial_top10_excel, label)
print('---Analysis of intervention methods completed！')

# # ----------------------------------------------lda clustering situation-----------------------
to_file = path + 'analysis_result/层次聚类_总体情况.xlsx'
label = 'label'
analysis_together.get_type_number(to_file, label)
# Month situation
paper_result_excel = path + 'analysis_result/层次聚类_发文量_论文_按月结果.xlsx'
trail_number_excel = path + 'analysis_result/层次聚类_发文量_试验_按月结果.xlsx'
all_number_excel = path + 'analysis_result/层次聚类_发文量_一起_按月结果.xlsx'
label_file = path + 'analysis_result/层次聚类_总体情况.xlsx'
label = 'label'
analysis_together.get_type_month(paper_result_excel, trail_number_excel, all_number_excel, label, label_file)
# Country situation
paper_number_excel = path + 'analysis_result/国家_发文量_论文.xlsx'
trail_number_excel = path + 'analysis_result/国家_发文量_试验.xlsx'
all_number_excel = path + 'analysis_result/国家_发文量_一起.xlsx'
paper_result_excel = path + 'analysis_result/层次聚类_论文top10_论文_按国家结果.xlsx'
trial_result_excel = path + 'analysis_result/层次聚类_试验top10_试验_按国家结果.xlsx'
all_result_excel = path + 'analysis_result/层次聚类_一起top10_一起_按国家结果.xlsx'
paper_top10_excel = path + 'analysis_result/层次聚类_一起top10_论文_按国家结果.xlsx'
trial_top10_excel = path + 'analysis_result/层次聚类_一起top10_试验_按国家结果.xlsx'
label = 'label'
analysis_together.country_top10_type(paper_number_excel, trail_number_excel, all_number_excel, paper_result_excel,
                        trial_result_excel, all_result_excel, paper_top10_excel, trial_top10_excel, label)
print('---lda cluster analysis is complete！')

# # ----------------------------------------------Cooperation network situation-----------------------
# # National Cooperation Network
df_paper_file_name = path + 'analysis_result/合作网络_论文_共现矩阵_按国家结果.xlsx'
node_paper_file_name = path + 'analysis_result/合作网络_论文_节点_按国家结果.xlsx'
triple_paper_file_name = path + 'analysis_result/合作网络_论文_边_按国家结果.xlsx'
df_trail_file_name = path + 'analysis_result/合作网络_试验_共现矩阵_按国家结果.xlsx'
node_trail_file_name = path + 'analysis_result/合作网络_试验_节点_按国家结果.xlsx'
triple_trail_file_name = path + 'analysis_result/合作网络_试验_边_按国家结果.xlsx'
df_all_file_name = path + 'analysis_result/合作网络_一起_共现矩阵_按国家结果.xlsx'
node_all_file_name = path + 'analysis_result/合作网络_一起_节点_按国家结果.xlsx'
triple_all_file_name = path + 'analysis_result/合作网络_一起_边_按国家结果.xlsx'
node_limit = 0
triple_limit = 0
analysis_together.get_country_co_network(df_paper_file_name, node_paper_file_name, triple_paper_file_name,
                                         df_trail_file_name, node_trail_file_name, triple_trail_file_name,
                                         df_all_file_name, node_all_file_name, triple_all_file_name,
                                         node_limit, triple_limit)
# # National Cooperation Network Conversion
node_paper_file_txt = path + 'analysis_result/合作网络_论文_节点_按国家结果.txt'
triple_paper_file_txt = path + 'analysis_result/合作网络_论文_边_按国家结果.txt'
node_trail_file_txt = path + 'analysis_result/合作网络_试验_节点_按国家结果.txt'
triple_trail_file_txt = path + 'analysis_result/合作网络_试验_边_按国家结果.txt'
node_all_file_txt = path + 'analysis_result/合作网络_一起_节点_按国家结果.txt'
triple_all_file_txt = path + 'analysis_result/合作网络_一起_边_按国家结果.txt'
analysis_together.get_txt_file(node_paper_file_name, node_paper_file_txt, True)
analysis_together.get_txt_file(node_trail_file_name, node_trail_file_txt, True)
analysis_together.get_txt_file(node_all_file_name, node_all_file_txt, True)
analysis_together.get_txt_file(triple_paper_file_name, triple_paper_file_txt, False)
analysis_together.get_txt_file(triple_trail_file_name, triple_trail_file_txt, False)
analysis_together.get_txt_file(triple_all_file_name, triple_all_file_txt, False)

# Institutional Cooperation Network
df_paper_file_name = path + 'analysis_result/合作网络_论文_共现矩阵_按机构结果.xlsx'
node_paper_file_name = path + 'analysis_result/合作网络_论文_节点_按机构结果.xlsx'
triple_paper_file_name = path + 'analysis_result/合作网络_论文_边_按机构结果.xlsx'
node_limit = 10
triple_limit = 0
analysis_together.get_org_co_network(df_paper_file_name, node_paper_file_name, triple_paper_file_name,
                                     node_limit, triple_limit)
node_paper_file_txt = path + 'analysis_result/合作网络_论文_节点_按机构结果.txt'
triple_paper_file_txt = path + 'analysis_result/合作网络_论文_边_按机构结果.txt'
analysis_together.get_txt_file(node_paper_file_name, node_paper_file_txt, True)
analysis_together.get_txt_file(triple_paper_file_name, triple_paper_file_txt, False)

# # Author cooperation network
df_paper_file_name = path + 'analysis_result/合作网络_论文_共现矩阵_按作者结果.xlsx'
node_paper_file_name = path + 'analysis_result/合作网络_论文_节点_按作者结果.xlsx'
triple_paper_file_name = path + 'analysis_result/合作网络_论文_边_按作者结果.xlsx'
df_trail_file_name = path + 'analysis_result/合作网络_试验_共现矩阵_按作者结果.xlsx'
node_trail_file_name = path + 'analysis_result/合作网络_试验_节点_按作者结果.xlsx'
triple_trail_file_name = path + 'analysis_result/合作网络_试验_边_按作者结果.xlsx'
df_all_file_name = path + 'analysis_result/合作网络_一起_共现矩阵_按作者结果.xlsx'
node_all_file_name = path + 'analysis_result/合作网络_一起_节点_按作者结果.xlsx'
triple_all_file_name = path + 'analysis_result/合作网络_一起_边_按作者结果.xlsx'
node_limit = 2
triple_limit = 0
analysis_together.get_author_co_network(df_paper_file_name, node_paper_file_name, triple_paper_file_name,
                                        df_trail_file_name, node_trail_file_name, triple_trail_file_name,
                                        df_all_file_name, node_all_file_name, triple_all_file_name,
                                        node_limit, triple_limit)
# # Cooperation network
node_paper_file_txt = path + 'analysis_result/合作网络_论文_节点_按作者结果.txt'
triple_paper_file_txt = path + 'analysis_result/合作网络_论文_边_按作者结果.txt'
node_trail_file_txt = path + 'analysis_result/合作网络_试验_节点_按作者结果.txt'
triple_trail_file_txt = path + 'analysis_result/合作网络_试验_边_按作者结果.txt'
node_all_file_txt = path + 'analysis_result/合作网络_一起_节点_按作者结果.txt'
triple_all_file_txt = path + 'analysis_result/合作网络_一起_边_按作者结果.txt'
analysis_together.get_txt_file(node_paper_file_name, node_paper_file_txt, True)
analysis_together.get_txt_file(node_trail_file_name, node_trail_file_txt, True)
analysis_together.get_txt_file(node_all_file_name, node_all_file_txt, True)
analysis_together.get_txt_file(triple_paper_file_name, triple_paper_file_txt, False)
analysis_together.get_txt_file(triple_trail_file_name, triple_trail_file_txt, False)
analysis_together.get_txt_file(triple_all_file_name, triple_all_file_txt, False)
print('---Cooperation network cooperation network analysis completed！')

# ----------------------------------------------Author situation-----------------------
# Each author's papers, experiments, total number of papers
paper_number_excel = path + 'analysis_result/作者_发文量_论文.xlsx'
trail_number_excel = path + 'analysis_result/作者_发文量_试验.xlsx'
all_number_excel = path + 'analysis_result/作者_发文量_一起.xlsx'
analysis_together.get_author_number(paper_number_excel, trail_number_excel, all_number_excel)
print('---Author analysis is complete！')

print('Analyze the content together！-------------------------------------------------------------------------------------')
