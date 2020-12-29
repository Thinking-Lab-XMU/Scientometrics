# -*- coding:utf-8 -*-
# @Time    : 2020/10/13 16:16
# @Author  : Heying Zhu

'''
The ID and DE are extracted, and the frequency of keywords is counted based on dictionary annotation on TI and AB
将ID和DE提取出来，并在TI和AB上基于词典标注，统计出关键词出现的频数
'''

import process.db as db
import spacy
import datetime
import pandas as pd
from spacy.lang.en import English
from spacy.pipeline import EntityRuler

save_root = "D:/data/middle_result/"
# relationship_color = ['#c23531','#2f4554', '#61a0a8', '#d48265', '#91c7ae','#749f83',  '#ca8622', '#bda29a','#6e7074']  # 9种


# 从数据库读取关键词（DE、ID）数据
def load_keyword_from_db():
    cnx, cursor = db.connect_db()
    # 查找出所有的ID和DE
    select_sql = "SELECT paper_id, ID, DE FROM paper"
    print(select_sql)
    results = db.select_muxu_data(cnx, cursor, select_sql)   # 每一篇文章的ID和DE
    print("共", len(results), "条数据")

    return results

# 从数据库读取论文（TI、AB）数据
def load_article_from_db():
    cnx, cursor = db.connect_db()
    # 查找出所有的TI和AB
    select_sql = "SELECT paper_id, TI, AB FROM paper"
    print(select_sql)
    results = db.select_muxu_data(cnx, cursor, select_sql)   # 每一篇文章的TI和AB
    print("共", len(results), "条数据")

    return results

# 从数据库中获取数据
def load_data_from_db(sql):
    cnx, cursor = db.connect_db()
    print("要执行的sql语句：", sql)
    results = db.select_muxu_data(cnx, cursor, sql)   # 每一篇文章的TI和AB
    print("共", len(results), "条数据")

    return results

# 从数据库中提取出个什么东西及它的频次
def extract_from_db():
    # 从数据库中提出org
    one_field_name = "financial_name"
    file_name = "资金来源列表"
    table_name = "paper_financial_new"
    sql = "SELECT " + one_field_name + ", count(DISTINCT paper_id) as num FROM " + table_name + " GROUP BY " + one_field_name
    results = load_data_from_db(sql)
    one_field_list = []
    count_list = []
    for result in results:
        one_field_list.append(result[0])
        count_list.append(result[1])
    data = pd.DataFrame({one_field_name: one_field_list, "count": count_list})
    data.to_csv(save_root + file_name + ".csv", index=False)

# ID和DE合并成一个列表（去重后）
def merge2list(results):
    ID_keywords_list = []
    DE_keywords_list = []
    for result in results:
        # ID处理
        if result[1] is not None:
            paper_keywords = result[1].split(";")
            for one_keyword in paper_keywords:
                # 不在关键词列表中，且长度大于2
                if one_keyword.strip() not in ID_keywords_list and one_keyword.strip() != "" and len(one_keyword.strip())>2:
                    ID_keywords_list.append(one_keyword.strip())
        # DE处理
        if result[2] is not None:
            paper_keywords = result[2].split(";")
            for one_keyword in paper_keywords:
                # 不在关键词列表中，且长度大于2
                if one_keyword.strip() not in DE_keywords_list and one_keyword.strip() != "" and len(one_keyword.strip())>2:
                    DE_keywords_list.append(one_keyword.strip())

    return ID_keywords_list, DE_keywords_list

# 将句子中的单词转换成标准格式
def word2lemma(nlp, sentence):
    doc_1 = nlp(sentence)
    lemma = [ token.lemma_ for token in doc_1]
    lemma_text = " ".join(lemma)

    doc_2 = nlp(lemma_text)
    lemma2 = [ token.lemma_ for token in doc_2]
    lemma2_text = " ".join(lemma2)

    return lemma2_text

# 将TI和AB合并成一个列表
def merge_TI_AB(results):
    paper_list = []
    nlp = spacy.load("en_core_web_sm")
    article_csv = pd.DataFrame(columns=("paper_id", "base_form"))

    # for result in results:
    for i in range(len(results)):
        if i % 100 == 0 and i != 0:
            print("已经处理", i, "条数据", datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S'))

        result = results[i]
        content = ""
        if result[1] is not None:
            lemma_text = word2lemma(nlp, result[1])
            content = content + lemma_text + "\n"
        if result[2] is not None:
            lemma_text = word2lemma(nlp, result[2])
            content = content + lemma_text
        paper_list.append(content)
        article_csv = article_csv.append([{"paper_id": result[0], "base_form": content}], ignore_index=True)

    article_csv.to_csv(save_root + "paper_basic_form.csv", index=False)
    return paper_list


# 将ID和DE词典转化成spacy的字典格式
def transform_dict_to_spacy(entity_dict):
    patterns = []
    for key, value in entity_dict.items():
        # for i in range(10):
        for i in range(len(value)):
            list_item = {}
            list_item['label'] = key.upper()
            list_item['id'] = value[i]
            pattern_list = []
            for word in value[i].split():
                pattern_list_item = {"LOWER" : word.lower()}
                pattern_list.append(pattern_list_item)
            list_item['pattern'] = pattern_list
            patterns.append(list_item)

    return patterns


# 将合并完同义词的list转化成spacy的字典格式
def transform_list_to_spacy(keyword_list):
    patterns = []

    for i in range(len(keyword_list)):
        list_item = {}
        list_item['label'] = "KEYWORD"
        list_item['id'] = keyword_list[i]
        # list_item['id'] = keyword_list[i].lower() if keyword_list[i].isupper() else keyword_list[i]
        pattern_list = []
        for word in keyword_list[i].split():
            pattern_list_item = {"LOWER" : word.lower()}
            pattern_list.append(pattern_list_item)
        list_item['pattern'] = pattern_list
        patterns.append(list_item)

    return patterns


# 在TI和AB上统计关键词的词频，传入的是ID和DE的原始列表
def get_freq1(ID_keywords_list, DE_keywords_list, paper_list, patterns):

    freq_data = pd.DataFrame({"keyword": ID_keywords_list+DE_keywords_list})
    freq_data['freq'] = 0
    nlp = English()
    ruler = EntityRuler(nlp)
    ruler.add_patterns(patterns)
    nlp.add_pipe(ruler)


    for i in range(len(paper_list)):
        paper = paper_list[i]
        if paper is None:
            continue
        if i % 100 == 0 and i != 0:
            print("已处理完", i, "篇摘要")

        # 对TI+AB进行基于词典的标注
        doc = nlp(paper)
        # 如果该篇文章含有关键词，则freq+1
        if len(doc.ents) != 0:
            for ent in doc.ents:
                num = freq_data.loc[freq_data['keyword'] == ent.ent_id_]
                num = num['freq'].to_list()[0]
                freq_data.loc[freq_data['keyword'] == ent.ent_id_, 'freq'] = num + 1

            # x = freq_data[freq_data['freq']>0]
    freq_data.to_csv(save_root + "keyword_freq1.csv", index=False)



# 在TI和AB上统计关键词的词频，传入的是ID和DE合并完同义词后的一个list
def get_freq2(keyword_list, paper_list, patterns):

    freq_data = pd.DataFrame({"keyword": keyword_list})
    freq_data['freq'] = 0
    nlp = English()
    ruler = EntityRuler(nlp)
    ruler.add_patterns(patterns)
    nlp.add_pipe(ruler)


    for i in range(len(paper_list)):
        paper = paper_list[i]
        if paper is None:
            continue
        if i % 100 == 0 and i != 0:
            print("已处理完", i, "篇摘要", datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S'))

        # 对TI+AB进行基于词典的标注
        doc = nlp(paper)
        # 如果该篇文章含有关键词，则freq+1
        if len(doc.ents) != 0:
            for ent in doc.ents:
                num = freq_data.loc[freq_data['keyword'] == ent.ent_id_]
                num = num['freq'].to_list()[0]
                freq_data.loc[freq_data['keyword'] == ent.ent_id_, 'freq'] = num + 1

            # x = freq_data[freq_data['freq']>0]
    freq_data = freq_data.sort_values(by="freq", ascending=False)
    freq_data.to_csv(save_root + "keyword_freq2.csv", index=False)
    print("词频统计结果保存至：", save_root + "keyword_freq2.csv")

# 根据同义词表获得一个同义词转换dict
def get_synonyms_transform():
    # 关键词文件保存路径
    file_path = "D:/data/thesaurus/alfalfa.the"
    synonyms_dict = {}
    normal_word = ""

    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    for line in lines:
        # 保存最近一个规范形式
        if line.startswith("**"):
            normal_word = line[2:-1]
            if normal_word.isupper():
                normal_word = normal_word.lower()
        # 如果为需要合并的同义词，则key为自己，value为规范形式
        elif line.startswith("0 1 ^") and line[5:-2].replace("\\", "") not in synonyms_dict.keys() and line[5:-2].replace("\\", "") != normal_word:
            synonyms_dict[line[5:-2].replace("\\", "")] = normal_word  # 保存自己与规范形式的转化
            # 如果该词全为大写，则将小写形式也存入
            if line[5:-2].isupper(): # and line[5:-2].lower() != normal_word :
                synonyms_dict[line[5:-2].replace("\\", "").lower()] = normal_word

    return synonyms_dict

# 合并ID和DE中的同义词
def merge_ID_DE_synonyms(entity_dict, synonyms_dict):
    keyword_list = []
    for key, value in entity_dict.items():
        for item in value:
            # 有同义词的将标准形式，且标准形式不再list中时，添加到list中
            if item in synonyms_dict.keys() and synonyms_dict[item].strip("\'") not in keyword_list:
                keyword_list.append(synonyms_dict[item].strip("\'"))
            # 没有同义词的则将自己添加到list中
            elif item.strip("\'") not in synonyms_dict.keys():
                keyword_list.append(item.strip("\'"))

    keyword_list = list(set(keyword_list))
    keyword_list.sort()
    return keyword_list




if __name__ == "__main__":

    print("开始读取关键词数据并转换成列表：", datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S'))
    # ID和DE
    ID_DE_results = load_keyword_from_db()
    # 关键词列表
    ID_keywords_list, DE_keywords_list = merge2list(ID_DE_results)
    # 将关键词合并成一个字典，并转换成spacy的Entity-Rule格式
    entity_dict = {"ID":ID_keywords_list, "DE":DE_keywords_list}

    # 将ID和DE的dict转成spacy可以识别的格式
    # patterns = transform_dict_to_spacy(entity_dict)

    print("生成同义词dict：", datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S'))
    synonyms_dict = get_synonyms_transform()    # 生成同义词合并字典

    print("合并ID和DE中的同义词：", datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S'))
    keyword_list = merge_ID_DE_synonyms(entity_dict, synonyms_dict)

    # 将合并完同义词的关键词list转成spacy可以识别的格式
    patterns = transform_list_to_spacy(keyword_list)


    print("\n开始读取论文数据并转换成列表：", datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S'))
    # TI和AB
    TI_AB_results = load_article_from_db()
    # 将TI和AB合并成一个list
    # paper_list = merge_TI_AB(TI_AB_results)   # 第一次运行
    paper_list = pd.read_csv(save_root + "paper_basic_form.csv", usecols=['base_form'])
    paper_list = paper_list['base_form'].to_list()


    print("\n开始统计词频：", datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S'))
    # 统计关键词出现的词频
    # get_freq1(ID_keywords_list, DE_keywords_list, paper_list, patterns)   # 初始的ID和DE统计词频
    get_freq2(keyword_list, paper_list, patterns)

    print("\n结束：", datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S'))


    # extract_from_db()


