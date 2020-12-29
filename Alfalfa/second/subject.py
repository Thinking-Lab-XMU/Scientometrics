# -*- coding:utf-8 -*-
# @Time    : 2020/10/21 10:43
# @Author  : Heying Zhu

'''
Interdisciplinary Statistics
交叉学科统计
'''

import process.db as db
import pandas as pd
import numpy as np

# 从数据库中获取数据
def load_data_from_db(sql):
    cnx, cursor = db.connect_db()
    print("sql:", sql)
    results = db.select_muxu_data(cnx, cursor, sql)   # 每一篇文章的TI和AB
    print("共", len(results), "条数据")

    return results

# 遍历从数据库中查询出的元组列表，统计学科共现次数
def count_co_occurrence(results):
    # 前10学科
    need_subject = ["Plant Sciences", "Agronomy", "Agriculture, Dairy & Animal Science", "Environmental Sciences",
                    "Agriculture, Multidisciplinary", "Biotechnology & Applied Microbiology",
                    "Biochemistry & Molecular Biology", "Food Science & Technology", "Genetics & Heredity",
                    "Soil Science", "Multidisciplinary Sciences", "Microbiology", "Entomology", "Veterinary Sciences",
                    "Ecology", "Horticulture", "Biology", "Cell Biology", "Water Resources", "Chemistry, Multidisciplinary",
                    "Biochemical Research Methods", "Chemistry, Applied", "Evolutionary Biology",
                    "Agricultural Engineering", "Energy & Fuels" ]   # 前25
    # need_subject = ["Plant Sciences", "Agronomy", "Agriculture, Dairy & Animal Science", "Environmental Sciences",
    #                 "Agriculture, Multidisciplinary", "Biotechnology & Applied Microbiology",
    #                 "Biochemistry & Molecular Biology", "Food Science & Technology", "Genetics & Heredity",
    #                 "Soil Science", "Multidisciplinary Sciences", "Microbiology", "Entomology", "Veterinary Sciences",
    #                 "Ecology", "Horticulture", "Biology", "Cell Biology", "Water Resources", "Chemistry, Multidisciplinary",
    #                 "Biochemical Research Methods", "Chemistry, Applied", "Evolutionary Biology", "Agricultural Engineering",
    #                 "Energy & Fuels", "Engineering, Environmental", "Chemistry, Analytical", "Toxicology",
    #                 "Engineering, Chemical", "Green & Sustainable Science & Technology", "Zoology", "Virology", "Mycology",
    #                 "Forestry", "Chemistry, Medicinal", "Nutrition & Dietetics", "Biophysics", "Meteorology & Atmospheric Sciences",
    #                 "Pharmacology & Pharmacy", "Endocrinology & Metabolism", "Engineering, Civil", "Geosciences, Multidisciplinary",
    #                 "Polymer Science", "Developmental Biology", "Physiology", "Biodiversity Conservation", "Marine & Freshwater Biology",
    #                 "Materials Science, Multidisciplinary", "Public, Environmental & Occupational Health", "Chemistry, Organic",
    #                 "Spectroscopy", "Immunology", "Materials Science, Paper & Wood", "Chemistry, Physical",
    #                 "Mathematical & Computational Biology", "Engineering, Electrical & Electronic",
    #                 "Environmental Studies", "Integrative & Complementary Medicine",
    #                 "Computer Science, Interdisciplinary Applications", "Fisheries", "Medicine, Research & Experimental",
    #                 "Oncology", "Agricultural Economics & Policy", "Microscopy", "Reproductive Biology",
    #                 "Geochemistry & Geophysics", "Materials Science, Textiles", "Nanoscience & Nanotechnology",
    #                 "Physics, Applied", "Remote Sensing", "Thermodynamics", "Geography, Physical",
    #                 "Instruments & Instrumentation", "Mathematics, Interdisciplinary Applications",
    #                 "Mechanics", "Medical Laboratory Technology", "Neurosciences",
    #                 "Radiology, Nuclear Medicine & Medical Imaging", "Behavioral Sciences",
    #                 "Computer Science, Information Systems", "Crystallography", "Economics", "Engineering, Mechanical",
    #                 "Engineering, Multidisciplinary", "Geography", "History & Philosophy Of Science",
    #                 "Medicine, General & Internal", "Mining & Mineral Processing", "Nuclear Science & Technology", "Ornithology",
    #                 "Physics, Atomic, Molecular & Chemical", "Surgery", "Urban Studies", "Anesthesiology", "Anthropology",
    #                 "Archaeology", "Astronomy & Astrophysics", "Chemistry, Inorganic & Nuclear", "Clinical Neurology",
    #                 "Computer Science, Artificial Intelligence", "Critical Care Medicine", "Engineering, Aerospace",
    #                 "Ethics", "Geology", "Imaging Science & Photographic Technology", "Infectious Diseases",
    #                 "Materials Science, Biomaterials", "Materials Science, Composites", "Medicine, Legal",
    #                 "Metallurgy & Metallurgical Engineering", "Mineralogy", "Ophthalmology", "Optics", "Parasitology",
    #                 "Physics, Condensed Matter", "Physics, Fluids & Plasmas", "Physics, Multidisciplinary",
    #                 "Regional & Urban Planning", "Rheumatology", "Social Sciences, Mathematical Methods",
    #                 "Sociology", "Statistics & Probability", "Telecommunications", "Transportation"]
    subject_list = []   # 学科list，长度为学科类别数
    paper_wc = []  # 5011篇论文的类别列表
    for result in results:
        if result[1] is None:
            continue
        wc_list = result[1].split(";")
        for one_wc in wc_list:
            if one_wc.strip() not in subject_list:
                subject_list.append(one_wc.strip())
        paper_wc.append(result[1])

    subject_list.sort()
    # 再遍历一遍统计学科共现次数
    co_occurrence_matrix = pd.DataFrame(columns=subject_list, index=subject_list)
    co_occurrence_matrix.loc[:, :] = 0
    for row in paper_wc:
        wc_list = row.split(";")
        if len(wc_list) > 1:
            for i in range(len(wc_list)):
                co_occurrence_matrix.loc[wc_list[i].strip(), wc_list[i].strip()] += 1
                for j in range(i+1, len(wc_list)):
                    co_occurrence_matrix.loc[wc_list[j].strip(), wc_list[i].strip()] += 1
                    co_occurrence_matrix.loc[wc_list[i].strip(), wc_list[j].strip()] += 1
    new_matrix = co_occurrence_matrix.loc[need_subject, need_subject]
    return need_subject, new_matrix

# 将共现矩阵转成画图的list格式
def matrix2list(co_occurrence_matrix):
    value_matrix = co_occurrence_matrix.values
    value = []

    for (x, y), i in np.ndenumerate(value_matrix):
        value.append([x, y, i])
    return value



def main():
    sql = "select paper_id, WC from paper"
    results = load_data_from_db(sql)
    subject_list, co_occurrence_matrix = count_co_occurrence(results)   # 获得学科共现矩阵
    # 将共现矩阵转成画图的list格式
    return subject_list, matrix2list(co_occurrence_matrix)



if __name__ == "__main__":
    main()