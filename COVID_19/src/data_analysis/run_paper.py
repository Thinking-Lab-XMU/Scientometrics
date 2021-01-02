from src.data_analysis import analysis_paper
from src.data_analysis import analysis_together
path = 'D:/zyx-project/paper/python_paper/'


# ----------------------------------------------Institutional situation-----------------------
# # Amount of papers issued by various institutions
paper_number_excel = path + 'analysis_result/论文_机构_发文量_论文.xlsx'
analysis_paper.get_org_number(paper_number_excel)
#
# # # Institution-top10 analysis paper
paper_number_excel = path + 'analysis_result/论文_机构_发文量_论文.xlsx'
paper_result_excel = path + 'analysis_result/论文_机构_发文量_top10.xlsx'
analysis_paper.get_org_top(paper_number_excel, paper_result_excel)
#
# # Monthly publication volume of institutions
paper_number_excel = path + 'analysis_result/论文_机构_发文量_论文.xlsx'
paper_result_excel = path + 'analysis_result/论文_机构_论文top10_论文_按月结果.xlsx'
analysis_paper.org_top10_month(paper_number_excel, paper_result_excel)

# # top10 organization classification system
paper_number_excel = path + 'analysis_result/论文_机构_发文量_论文.xlsx'
paper_result_excel = path + 'analysis_result/论文_机构_论文top10_论文_介入手段.xlsx'
label = 'topic'
analysis_paper.org_top10_intervention(paper_number_excel, paper_result_excel, label)
#
# # Top10 institutions clustering
paper_number_excel = path + 'analysis_result/论文_机构_发文量_论文.xlsx'
paper_result_excel = path + 'analysis_result/论文_机构_论文top10_论文_层次聚类.xlsx'
label = 'label'
analysis_paper.org_top10_type(paper_number_excel, paper_result_excel, label)
#
print('---Institutional analysis completed！')

# ----------------------------------------------Journal situation-----------------------
# Number of papers published in each journal
paper_number_excel = path + 'analysis_result/论文_期刊_发文量_论文.xlsx'
analysis_paper.get_publish_number(paper_number_excel)
#
# # # Monthly publication volume of journals
paper_number_excel = path + 'analysis_result/论文_期刊_发文量_论文.xlsx'
paper_result_excel = path + 'analysis_result/论文_期刊_论文top10_论文_按月结果.xlsx'
analysis_paper.publish_top10_month(paper_number_excel, paper_result_excel)


# ----------------------------------------------Subject situation-----------------------
# Amount of papers published in various subject
paper_number_excel = path + 'analysis_result/论文_学科_发文量_论文.xlsx'
analysis_paper.get_wc_number(paper_number_excel)
#
# # # Discipline monthly publication volume
paper_number_excel = path + 'analysis_result/论文_学科_发文量_论文.xlsx'
paper_result_excel = path + 'analysis_result/论文_学科_论文top10_论文_按月结果.xlsx'
analysis_paper.wc_top10_month(paper_number_excel, paper_result_excel)

# # volume country
paper_number_excel = path + 'analysis_result/论文_学科_发文量_论文.xlsx'
country_number_excel = path + 'analysis_result/国家_发文量_论文.xlsx'
paper_result_excel = path + 'analysis_result/论文_学科_top10_论文_按国家结果.xlsx'
analysis_paper.wc_top10_country(paper_number_excel, country_number_excel, paper_result_excel)

# Interdisciplinary (cooperative network)
paper_number_excel = path + 'analysis_result/论文_学科_发文量_论文.xlsx'
df_paper_file_name = path + 'analysis_result/论文_学科_共现矩阵.xlsx'
df_top10_file_name = path + 'analysis_result/论文_学科_top20_共现矩阵.xlsx'
node_all_file_name = path + 'analysis_result/论文_学科_共现矩阵_点.xlsx'
triple_all_file_name = path + 'analysis_result/论文_学科_共现矩阵_边.xlsx'
analysis_paper.wc_network(paper_number_excel, df_paper_file_name, df_top10_file_name, node_all_file_name, triple_all_file_name, 0, 0)
node_all_file_txt = path + 'analysis_result/论文_学科_共现矩阵_点.txt'
triple_all_file_txt = path + 'analysis_result/论文_学科_共现矩阵_边.txt'
analysis_together.get_txt_file(node_all_file_name, node_all_file_txt, True)
analysis_together.get_txt_file(triple_all_file_name, triple_all_file_txt, False)
