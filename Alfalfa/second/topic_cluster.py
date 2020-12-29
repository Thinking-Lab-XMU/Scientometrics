# -*- coding:utf-8 -*-
# @Time    : 2020/10/23 14:27
# @Author  : Heying Zhu

'''
LDA topic cluster
主题聚类
'''

import numpy as np
import lda
import lda.datasets
import pandas as pd
import process.db as db
import spacy
from spacy.pipeline import EntityRuler
import datetime


n_topic = 10  # 主题数
n_top_words = 20  # 显示的关键词数量
n_iter = 1000  # lda的迭代次数
n_paper = 25   # 要输出的前n篇文章的TI
flag_dict = {1: "all",        # 所有数据的主题聚类
             2: "2009-2012",  # 2009-2012数据的主题聚类
             3: "2013-2016",  # 2013-2016数据的主题聚类
             4: "2017-2020"}  # 2017-2020数据的主题聚类
select_sql_dict = {
    1: "SELECT paper_id, TI, AB, ID, DE, PY FROM paper",
    2: "SELECT paper_id, TI, AB, ID, DE, PY FROM paper WHERE PY >= 2009 AND PY <= 2012",
    3: "SELECT paper_id, TI, AB, ID, DE, PY FROM paper WHERE PY >= 2013 AND PY <= 2016",
    4: "SELECT paper_id, TI, AB, ID, DE, PY FROM paper WHERE PY >= 2017 AND PY <= 2020"
}

# 专家对主题聚类的命名结果
topic_name = {"2009-2012": ["1生长发育与生物合成调控", "2生物修复", "3抗非生物胁迫", "4饲料营养成分", "4饲养价值", "5菌根共生机制研究",
                            "10遗传多样性研究", "0其他", "7田间生产与环境影响", "8昆虫生态"],
              "2013-2016": ["0其他1", "4饲养价值", "0其他2", "1生长发育与生物合成调控", "9种子处理", "5菌根共生机制研究", "10遗传多样性研究",
                            "8昆虫生态", "0其他（2+7）", "3抗非生物胁迫"],
              "2017-2020": ["9种子处理", "11生物活性成分", "8病毒与昆虫生态", "2生物修复", "5菌根共生机制研究", "4青贮发酵及饲料品质",
                            "10遗传多样性研究", "4饲养价值", "7田间生产", "3抗非生物胁迫"],
              "all": ["2生物修复", "5菌根共生机制研究", "7田间生产", "8昆虫生态", "4饲养价值", "9种子处理", "11生物活性成分", "7田间生产",
                      "3抗非生物胁迫", "0其他（1+3）"]}


flag = 1


# 使用示例
def use_test():
    # document-term matrix
    X = lda.datasets.load_reuters()
    vocab = lda.datasets.load_reuters_vocab()
    titles = lda.datasets.load_reuters_titles()

    model = lda.LDA(n_topics=20, n_iter=500, random_state=1)
    model.fit(X)  # model.fit_transform(X) is also available
    topic_word = model.topic_word_  # model.components_ also works
    n_top_words = 20

    # 输出主题词
    for i, topic_dist in enumerate(topic_word):
        topic_words = np.array(vocab)[np.argsort(topic_dist)][:-(n_top_words+1):-1]
        print('Topic {}: {}'.format(i, ' '.join(topic_words)))

    # 输出
    doc_topic = model.doc_topic_
    for i in range(20):
        print("{} (top topic: {})".format(titles[i], doc_topic[i].argmax()))

    print("ddd")


# 苜蓿的聚类从这里开始

# 从清洗后得到的csv中得到关键词列表（之后要删除无意义词）——》得到vocab
def get_keyword_list():
    path = "D:/heying/小论文/苜蓿/中间结果1014/关键词词频统计结果-合并完同义词后.csv"

    with open(path) as f:
        keyword_df = pd.read_csv(f)

    keyword_list = keyword_df['keyword'].str.lower().to_list()
    keyword_list = list(set(keyword_list))
    keyword_list.sort()

    keyword_list = clean_meaningless(keyword_list)
    return tuple(keyword_list)

# 将无意义词去除
def clean_meaningless(keyword_list):
    meaningless_list = ["effect", "study", "year", "use", "high", "matter", "low", "increase", "compare", "decrease",
                        "result", "rate", "different", "total", "content", "analysis", "control", "experiment",
                        "application", "suggest", "identify", "development", "number",
                        "significantly", "affect", "value", "group", "show", "expression", "log", "level",
                        "reduce", "period", "great", "change", "role", "extract", "extraction", "method",
                        "uptake", "field", "grow", "day", "plant", "significant", "express",
                        "determine", "factor", "condition", "activity", "growth", "involve", "wall", "respectively",
                        "function", "induce"]
    for one_word in meaningless_list:
        if one_word in keyword_list:
            keyword_list.remove(one_word)
    return keyword_list


# 从数据库中获取TI、AB、DE、ID和PY
def load_from_db(select_sql):
    cnx, cursor = db.connect_db()
    # # 查找出所有的ID和DE
    # select_sql = "SELECT paper_id, TI, AB, ID, DE FROM paper"
    print(select_sql)
    results = db.select_muxu_data(cnx, cursor, select_sql)   # 每一篇文章的TI、AB、DE和ID
    print("共", len(results), "条数据")

    return results


# 数据库的tuple格式转换——》生成titles和content
def get_title_and_content(results):
    # TI的列表，最后会转成元组返回
    title_list = []
    # 要计算词频矩阵的文本list
    content_list= []
    # 年份
    year_list = []
    # 论文编号
    no_list = []

    for result in results:
        no_list.append(result[0])
        # 将TI加入到title_list中
        if result[1] is not None:
            title_list.append(result[1])
        else:
            title_list.append("")

        # 将TI加入到title_list中
        if result[5] is not None:
            year_list.append(result[5])
        else:
            year_list.append("")

        # 将四个字段拼接在一起
        content = ""
        for i in range(1, len(result)-1):
            if result[i] is not None:
                content = content + result[i] + "\n"
        content_list.append(content)

    return tuple(title_list), content_list, year_list, no_list


# 将ID和DE词典转化成spacy的字典格式
def transform_dict_to_spacy(keyword_tuple):
    patterns = []

    for i in range(len(keyword_tuple)):
        list_item = {}
        list_item['label'] = "KEY"
        list_item['id'] = keyword_tuple[i]
        pattern_list = []
        for word in keyword_tuple[i].split():
            pattern_list_item = {"LOWER" : word.lower()}
            pattern_list.append(pattern_list_item)
        list_item['pattern'] = pattern_list
        patterns.append(list_item)

    return patterns


# 在TI+AB+ID+DE上，计算词频矩阵——》X
def calculate_word_freq_matrix(content_list, keyword_tuple, patterns, suffix, is_save=False):

    root_path = "D:/heying/小论文/苜蓿/中间结果1014/"
    freq_matrix = np.zeros((len(content_list), len(keyword_tuple)), dtype=np.int)
    keyword_list = list(keyword_tuple)
    npy_file_name = root_path + "freq_matrix_" + str(len(content_list)) + "_" + str(len(keyword_tuple)) + \
                    "_" + suffix + ".npy"

    if is_save:
        # 加载spacy模型
        nlp = spacy.load("en_core_web_sm")
        ruler = EntityRuler(nlp)
        ruler.add_patterns(patterns)
        nlp.add_pipe(ruler)
        nlp.remove_pipe('ner')


        for i in range(len(content_list)):
            paper = content_list[i]
            if i % 100 == 0 and i != 0:
                print("已处理完", i, "篇论文", datetime.datetime.now().strftime('%Y.%m.%d-%H:%M:%S'))

            # 对TI+AB+ID+DE进行基于词典的标注
            doc = nlp(paper)
            # 如果该篇文章含有关键词，则freq+1
            if len(doc.ents) != 0:
                for ent in doc.ents:
                    j = keyword_list.index(ent.ent_id_)
                    freq_matrix[i][j] += 1


        np.save(npy_file_name, freq_matrix)  # 将numpy数组保存下来
        print("词频矩阵X保存至：", npy_file_name)
    else:
        freq_matrix = np.load(npy_file_name)  # 直接读取
    freq_matrix = freq_matrix.astype(int)
    return freq_matrix


# 根据nzw（主题-关键词矩阵，shape:[n_topic, len(keywords]）计算主题间的相关性
def calculate_topic_relevance(nzw_):
    relevance_dict = {}
    for i in range(nzw_.shape[0]):
        # x = nzw_[i]  # .reshape(nzw_.shape[1], 1)
        x = np.mat(nzw_[i])
        for j in range(i+1, nzw_.shape[0]):
            # y = nzw_[j]  # .reshape(nzw_.shape[1], 1)
            y = np.mat(nzw_[j])
            # relevance_dict[str(i) + "-" + str(j)] = np.sum(np.sqrt((x-y)**2))    # 欧式距离
            relevance_dict[str(i) + "-" + str(j)] = (float(x * y.T)/(np.linalg.norm(x) * np.linalg.norm(y)))  # 余弦相似度
    print("计算主题间的相关性阵完成！")
    return relevance_dict


# 苜蓿lda主题聚类
def muxu_lda(X, vocab, titles, suffix, year_list, is_save=False):
    path = "D:/heying/小论文/苜蓿/第二次/lda_topic_" + str(X.shape[0]) + "_" + str(X.shape[1]) + "_" + suffix + ".xlsx"
    writer = pd.ExcelWriter(path)

    # document-term matrix : X, vocab, titles
    model = lda.LDA(n_topics=n_topic, n_iter=n_iter, random_state=1)
    model.fit(X)  # model.fit_transform(X) is also available
    topic_word = model.topic_word_  # model.components_ also works

    topic_word_dict = {}   # 每个主题的主题词列表字典
    word_score_dict = {}   # 每个单词最高得分及出现的主题id
    topic_word_list = []   # 每个主题的主题词列表
    topic_size = []

    # 根据nzw（主题-关键词矩阵，shape:[n_topic, len(keywords]）计算主题间的相关性
    calculate_topic_relevance(model.nzw_)

    # 输出主题词（硬划分之前）
    soft_divide = pd.DataFrame()
    print("\n原始LDA的聚类结果：")
    for i, topic_dist in enumerate(topic_word):
        topic_words = np.array(vocab)[np.argsort(topic_dist)][:-(n_top_words+1):-1]
        words_score = topic_dist[np.argsort(topic_dist)][:-(n_top_words+1):-1]
        topic_word_list.append(topic_words)
        print_list = []   # 将两个array组合在一起
        for j in range(n_top_words):
            score = words_score[j]
            word = topic_words[j]
            print_list.append(str(score)[:5] + "*\"" + str(word) + "\"")

            # 硬划分拆分
            if word in word_score_dict.keys() and word_score_dict[word]["score"] < float(score):
                word_score_dict[word]["score"] = float(str(score)[:5])
                word_score_dict[word]["topic"] = i
            elif word not in word_score_dict.keys():
                word_score_dict[word] = {}
                word_score_dict[word]["score"] = float(str(score)[:5])
                word_score_dict[word]["topic"] = i
        print("Topic {} : {}".format(i, " + ".join(print_list)))  # 输出每个主题的关键词及其得分（硬划分之前）
        # soft_divide = soft_divide.append([{"topic": i, "keyword": " + ".join(print_list)}], ignore_index=True)
        soft_divide = soft_divide.append([{"topic": i, "keyword": " + ".join(topic_words)}], ignore_index=True)   # 不加关键词分数
    soft_divide.to_excel(writer, sheet_name="soft_divide", index=False)

    # 硬划分组合
    for key, value in word_score_dict.items():
        if value["topic"] in topic_word_dict.keys():
            # topic_word_dict[value["topic"]].append(str(value["score"]) + "*\"" + key + "\"")
            topic_word_dict[value["topic"]].append(key)
        else:
            topic_word_dict[value["topic"]] = []
            # topic_word_dict[value["topic"]].append(str(value["score"]) + "*\"" + key + "\"")
            topic_word_dict[value["topic"]].append(key)

    # 输出每个主题的主题词（硬划分之后）
    hard_divide = pd.DataFrame()
    print("\n硬划分后的结果：")
    for i in sorted (topic_word_dict):
        hard_words = sorted(topic_word_dict[i], reverse=True)
        print("Topic", i, ": ", hard_words)
        hard_divide = hard_divide.append([{"topic": i, "keyword": hard_words}], ignore_index=True)
    hard_divide.to_excel(writer, sheet_name="hard_divide", index=False)


    # 输出每个类别概率最高的15篇文章标题
    top_15_per_category = pd.DataFrame()
    print("\n\n")
    doc_topic = model.doc_topic_
    doc_topic_df = pd.DataFrame(doc_topic, columns=[i for i in range(n_topic)], index=[i for i in range(len(titles))])
    doc_topic_df['final_score'] = doc_topic_df.max(axis=1)     # 每一行的最大值
    doc_topic_df['final_topic'] = doc_topic_df.idxmax(axis=1)  # 每一行最大值的索引

    for i in range(n_topic):
        temp_df = doc_topic_df.loc[doc_topic_df['final_topic'] == i]
        temp_df = temp_df[['final_score', "final_topic"]]
        temp_df.sort_values(by="final_score", inplace=True, ascending=False)
        topic_size.append(temp_df.shape[0])
        top_index = list(temp_df.index)[:n_paper]

        print("\nTopic ", i, " : ")
        for j in range(len(top_index)):
            print(j, " : ", titles[top_index[j]])
            top_15_per_category = top_15_per_category.append([{"topic":i, "paper_no": j, "TI": titles[top_index[j]], "PY": year_list[top_index[j]]}], ignore_index=True)
    top_15_per_category.to_excel(writer, sheet_name="top_15_per_category", index=False)

    if is_save:
        print("lda聚类结果保存至：", path)
        writer.save()
    writer.close()

    X_plus = pd.DataFrame(X)
    X_plus['final_topic'] = doc_topic_df['final_topic']

    return X_plus, topic_word_list, topic_size, model.nzw_


# 计算战略坐标, 主题-主题矩阵（5011*5011）计算战略坐标，第一种方式
def calculate_strategic_coordinates(X_plus):
    root_path = "D:/heying/小论文/苜蓿/中间结果1014/"
    density_list = []
    center_list = []

    # 所有论文的共词矩阵
    # X = X_plus.iloc[:, :-1].values
    # paper_array = np.dot(X, X.T)
    # np.save(root_path + "paper_array.npy", paper_array)  # 将numpy数组保存下来
    paper_array = np.load(root_path + "paper_array.npy")  # 直接读取

    # 密度计算
    # 对于每个主题
    for i in range(n_topic):
        temp_df = X_plus.loc[X_plus['final_topic'] == i]   # 该主题下的词频矩阵
        topic_index = list(temp_df.index)

        # 保留同组的数据
        density_matrix = paper_array[topic_index, :]
        density_matrix = density_matrix[:, topic_index]  # 主题的共词矩阵
        # 将对角线置零
        row_list = [j for j in range(density_matrix.shape[0])]
        density_matrix[row_list, row_list] = 0
        # 求每一行的和, 和的均值为密度
        density_list.append(np.mean(np.sum(density_matrix, axis=1)))

        # 向心度计算
        # 删除同组的数据
        center_matrix = paper_array[topic_index, :]
        center_matrix = center_matrix[:,[ j for j in list(X_plus.index) if j not in topic_index]]
        # 求每一行的和, 和的均值为密度
        center_list.append(np.mean(np.sum(center_matrix, axis=1)))


    return density_list, center_list


# 主题词-主题词矩阵（17553*17553）计算战略坐标，第二种方式
def calculate_strategic_coordinates2(X, topic_word_list, keyword_tuple, topic_size):
    root_path = "D:/heying/小论文/苜蓿/中间结果1014/"
    keyword_list = list(keyword_tuple)
    density_list = []
    center_list = []

    # 构造词-词矩阵
    # Y = X.astype(float)
    # all_word_array = np.dot(Y.T, Y)
    # all_word_array = all_word_array.astype(int)
    # np.save(root_path + "all_word_array.npy", all_word_array)  # 将numpy数组保存下来
    all_word_array = np.load(root_path + "all_word_array.npy")  # 直接读取

    # 密度计算
    for one_topic_list in topic_word_list:   # 一个主题里的关键词列表
        D = 0
        for i in range(len(one_topic_list)):
            x_index = keyword_list.index(one_topic_list[i])
            for j in range(len(one_topic_list)):
                if i == j :
                    continue
                y_index = keyword_list.index(one_topic_list[j])
                D = D + all_word_array[x_index, y_index]
        density_list.append(D/len(one_topic_list)/(len(one_topic_list)-1))

    # 向心度计算
    for topic_i in range(len(topic_word_list)):   # 第i个主题
        C = 0
        for word_x in topic_word_list[topic_i]:     # 第i个主题的第x个词
            x_index = keyword_list.index(word_x)
            for topic_j in range(len(topic_word_list)):   # 第j个主题，若为自己则跳过
                if topic_i == topic_j:
                    continue
                for word_y in topic_word_list[topic_j]: # 第j个主题的第y个词
                    y_index = keyword_list.index(word_y)
                    C = C + all_word_array[x_index, y_index]
        center_list.append(C)

    print_d_c(density_list, center_list, topic_size)

    return all_word_array

# 将密度、向心度输出，可以直接粘贴到json里
def print_d_c(density_list, center_list, topic_size):

    marksData = []
    print("marksData开始输出！")

    for i in range(1, n_topic+1):
        one_item = {}
        one_item['name'] = "Topic" + str(i)
        one_item['value'] = [center_list[i-1], density_list[i-1]]
        one_item['symbolSize'] = topic_size[i-1]/10
        marksData.append(one_item)

    for one_item in marksData:
        print("{")
        for key, value in one_item.items():
            if type(value) == str:
                print("\t" + key + ": '" + value + "',")
            else:
                print("\t" + key + ": " + str(value) + ",")
        print("},")

    print("marksData输出完毕！")

    print("\n中心点坐标开始输出！")
    print("xAxis:", np.mean(center_list))
    print("yAxis:", np.mean(density_list))
    print("中心点坐标输出完毕！")

    print("\nmax_x:", max(center_list))
    print("min_x:", min(center_list))
    print("max_y:", max(density_list))
    print("min_y:", min(density_list))


# 将从数据库中查询出来的对应国家的paper_id元组转化成list
def tuple2list(paper_id_tuple):
    paper_id_list = []
    for item in paper_id_tuple:
        paper_id_list.append(item[0])

    return paper_id_list


# 处理一个数据集的总流程
def process(flag1, keyword_tuple, patterns):
    print("从数据库获取数据...", datetime.datetime.now().strftime('%Y.%m.%d-%H:%M:%S'))

    print("获取" + flag_dict[flag1] + "论文数据...")
    db_results = load_from_db(select_sql_dict[flag1])        # 查找出所有的TI、AB、ID和DE


    titles, content_list, year_list, no_list = get_title_and_content(db_results)   # 遍历后格式转换

    print("开始计算词频矩阵...", datetime.datetime.now().strftime('%Y.%m.%d-%H:%M:%S'))
    freq_matrix = calculate_word_freq_matrix(content_list, keyword_tuple, patterns, suffix=flag_dict[flag1], is_save=False) # X

    print("开始主题聚类...", datetime.datetime.now().strftime('%Y.%m.%d-%H:%M:%S'))
    X_plus, topic_word_list, topic_size, nzw_ = muxu_lda(X=freq_matrix, vocab=keyword_tuple, titles=titles, suffix=flag_dict[flag1], year_list=year_list, is_save=False)

    X_plus.index = no_list
    return db_results, X_plus, nzw_

# 根据主题号获取主题名称
def get_topic_all(row):
    return topic_name[flag_dict[1]][row]

def get_topic_2(row):
    return topic_name[flag_dict[2]][row]

def get_topic_3(row):
    return topic_name[flag_dict[3]][row]

def get_topic_4(row):
    return topic_name[flag_dict[4]][row]


# 根据nzw（主题-关键词矩阵，shape:[n_topic, len(keywords]）计算主题间的相关性（相邻两个阶段的主题相似度）
def calculate_topic_relevance_diff_stage(nzw_):
    # 中文版
    topic_name = {0:"1-生长发育与生物合成调控", 1: "1-生物修复", 2: "1-抗非生物胁迫", 3: "1-饲料营养成分", 4: "1-饲养价值",
                  5: "1-菌根共生机制研究", 6:"1-遗传多样性研究", 7: "1-其他", 8: "1-田间生产与环境影响", 9: "1-昆虫生态",          # 2009-2012
                  10: "2-其他1", 11: "2-饲养价值", 12: "2-其他2", 13: "2-生长发育与生物合成调控", 14: "2-种子处理",
                  15: "2-菌根共生机制研究", 16: "2-遗传多样性研究", 17: "2-昆虫生态", 18: "2-其他3", 19: "2-抗非生物胁迫",         # 2013-2016
                  20: "3-种子处理", 21: "3-生物活性成分", 22: "3-病毒与昆虫生态", 23: "3-生物修复", 24: "3-菌根共生机制研究",
                  25: "3-青贮发酵及饲料品质", 26: "3-遗传多样性研究", 27: "3-饲养价值", 28: "3-田间生产", 29: "3-抗非生物胁迫"}

    # 英文版
    topic_name = {0:"1-Growth and synthesis regulation", 1: "1-Bioremediation", 2: "1-Resistance to abiotic stress", 3: "1-Feed nutrition", 4: "1-Feeding value",
                  5: "1-Mechanism of mycorrhizal symbiosis", 6:"1-Genetic diversity research", 7: "1-Cannot name exactly", 8: "1-Field production and environmental impact", 9: "1-Insect ecology",          # 2009-2012
                  10: "2-Cannot name exactly1", 11: "2-Feeding value", 12: "2-Cannot name exactly2", 13: "2-Growth and synthesis regulation", 14: "2-Seed treatment",
                  15: "2-Mechanism of mycorrhizal symbiosis", 16: "2-Genetic diversity research", 17: "2-Insect ecology", 18: "2-Cannot name exactly3", 19: "2-Resistance to abiotic stress",         # 2013-2016
                  20: "3-Seed treatment", 21: "3-Biologically active ingredients", 22: "3-Virus and insect ecology", 23: "3-Bioremediation", 24: "3-Mechanism of mycorrhizal symbiosis",
                  25: "3-Silage fermentation and feed quality", 26: "3-Genetic diversity research", 27: "3-Feeding value", 28: "3-Field production", 29: "3-Resistance to abiotic stress"}




    topic_size = {0: 148, 1: 131, 2: 143, 3: 118, 4: 163, 5: 162, 6: 212, 7: 149, 8: 140, 9: 107,          # 2009-2012
                      10: 143, 11: 184, 12: 141, 13: 246, 14: 162, 15: 189, 16: 167, 17: 103, 18: 164, 19: 199,         # 2013-2016
                      20: 133, 21: 115, 22: 144, 23: 178, 24: 324, 25: 147, 26: 131, 27: 177, 28: 251, 29: 240}


    relevance_dict = {}
    links = []

    for i in range(nzw_.shape[0]):
        relevance_dict[i] = {}
        # x = nzw_[i]  # .reshape(nzw_.shape[1], 1)
        x = np.mat(nzw_[i])
        for j in range(i+1, nzw_.shape[0]):
            if j >= (int(i/10)+1)*10 and j <= (int(i/10)+2)*10-1:
                # y = nzw_[j]  # .reshape(nzw_.shape[1], 1)
                y = np.mat(nzw_[j])
                # relevance_dict[str(i) + "-" + str(j)] = np.sum(np.sqrt((x-y)**2))    # 欧式距离
                relevance_dict[i][j] = (float(x * y.T)/(np.linalg.norm(x) * np.linalg.norm(y)))  # 余弦相似度
    print("计算主题间的相关性阵完成！")

    # # 计算相似度占比
    for key_1, value_1 in relevance_dict.items():
        for key_2, value_2 in value_1.items():
            value = value_2/sum(list(relevance_dict[key_1].values()))
            if value >= 0.12:
                one_link = {"source": topic_name[key_1], "target": topic_name[key_2], "value": topic_size[key_1]*value,
                            "lineStyle": {"color": "source", "opacity":0.2}}
                links.append(one_link)
            else:
                one_link = {"source": topic_name[key_1], "target": topic_name[key_2], "value": topic_size[key_1]*value,
                            "lineStyle": {"color": "white", "opacity": 0}}
                links.append(one_link)

    print(links)
    return relevance_dict, links


# 时序主题分析
def time_topic():
    # 查看论文流向
    all_topic_df = pd.DataFrame(columns=['2009-2012', '2013-2016', '2017-2020', 'all'])
    db_results_1, X_plus_1, nzw_1 = process(1, keyword_tuple, patterns)   # all
    all_topic_df['all'] = X_plus_1['final_topic'].apply(get_topic_all)
    db_results_2, X_plus_2, nzw_2 = process(2, keyword_tuple, patterns)   # 2009-2012
    all_topic_df['2009-2012'] = -1
    all_topic_df.loc[X_plus_2.index, '2009-2012'] = X_plus_2['final_topic'].apply(get_topic_2)
    db_results_3, X_plus_3, nzw_3 = process(3, keyword_tuple, patterns)   # 2013-2016
    all_topic_df['2013-2016'] = -1
    all_topic_df.loc[X_plus_3.index, '2013-2016'] = X_plus_3['final_topic'].apply(get_topic_3)
    db_results_4, X_plus_4, nzw_4 = process(4, keyword_tuple, patterns)   # 2017-2020
    all_topic_df['2017-2020'] = -1
    all_topic_df.loc[X_plus_4.index, '2017-2020'] = X_plus_4['final_topic'].apply(get_topic_4)
    # all_topic_df.to_excel("D:/heying/小论文/苜蓿/第二次/topic_time.xlsx")

    # 各个阶段主题-关键词矩阵的合并
    nzw = np.concatenate((nzw_2, nzw_3), axis=0)
    nzw = np.concatenate((nzw, nzw_4), axis=0)
    # nzw = np.concatenate((nzw, nzw_1), axis=0)
    relevance_dict, links = calculate_topic_relevance_diff_stage(nzw)   # to draw picture
    return relevance_dict, links




if __name__ == "__main__":
    # use_test()   # 使用示例

    # 苜蓿主题聚类从这里开始
    print("从csv中获取清洗后的关键词列表...", datetime.datetime.now().strftime('%Y.%m.%d-%H:%M:%S'))
    keyword_tuple = get_keyword_list()  # vocab

    print("转成spacy可以识别的格式...", datetime.datetime.now().strftime('%Y.%m.%d-%H:%M:%S'))
    patterns = transform_dict_to_spacy(keyword_tuple)

    print("从数据库获取数据...", datetime.datetime.now().strftime('%Y.%m.%d-%H:%M:%S'))

    # # 所有数据，包括总的和分为三个阶段的数据，最后合成一个
    # four_db_results = {}
    # for flag in range(1, 5):
    #     print("获取" + flag_dict[flag] + "论文数据...")
    #     db_results = load_from_db(select_sql_dict[flag])# 查找出所有的TI、AB、ID和DE
    #     four_db_results[flag] = db_results
    # 单个的阶段的数据
    print("获取" + flag_dict[flag] + "论文数据...")
    db_results = load_from_db(select_sql_dict[flag])        # 查找出所有的TI、AB、ID和DE


    titles, content_list, year_list = get_title_and_content(db_results)   # 遍历后格式转换

    print("开始计算词频矩阵...", datetime.datetime.now().strftime('%Y.%m.%d-%H:%M:%S'))
    freq_matrix = calculate_word_freq_matrix(content_list, keyword_tuple, patterns, suffix=flag_dict[flag], is_save=False) # X

    print("开始主题聚类...", datetime.datetime.now().strftime('%Y.%m.%d-%H:%M:%S'))
    X_plus, topic_word_list, topic_size = muxu_lda(X=freq_matrix, vocab=keyword_tuple, titles=titles, suffix=flag_dict[flag], year_list=year_list, is_save=False)

    # 计算战略坐标
    print("开始计算战略坐标...", datetime.datetime.now().strftime('%Y.%m.%d-%H:%M:%S'))
    # # calculate_strategic_coordinates(X_plus)   # 主题-主题矩阵（5011*5011）计算战略坐标，第一种方式
    all_word_array = calculate_strategic_coordinates2(freq_matrix, topic_word_list, keyword_tuple, topic_size)  # 主题词-主题词矩阵（17537*17537）计算战略坐标，第二种方式


    print(":dgdfsa")
