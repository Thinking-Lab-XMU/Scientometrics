import string

import gensim
from gensim.models import CoherenceModel
from sklearn import manifold
from sklearn.cluster import KMeans

from src.data_process import wetlandEntityAnnotation
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from pylab import mpl

mpl.rcParams['font.sans-serif'] = ['SimHei']
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
from gensim import corpora
import numpy as np
import pyLDAvis
import pyLDAvis.gensim
import spacy


# ---------------------Keyword matching (text processing)---------------------------------
def clean_keyword(doc, patterns, synonyms_dict):
    """
    Clean with keywords
    :param doc:
    :param patterns:
    :param synonyms_dict:
    :return:
    """
    stop_word = ['treatment', 'vaccines', 'pneumonia', 'therapy', 'syndrome']
    # 括号前面加空格
    doc = doc.replace('(', ' (')
    # 命名实体识别, 进行同义词替换和 加_防止分开
    entities = wetlandEntityAnnotation.spacy_ner_basedon_dict_2(doc, patterns)
    add = 0
    stop_free = []
    for entity in entities:
        start = entity[0]
        end = entity[1]
        if synonyms_dict.__contains__(entity[2]):
            result = synonyms_dict[entity[2]]
            text_replace = result.replace(' ', '_')
            doc = doc[:start + add] + text_replace + doc[end + add:]
            add = add + len(result) - (end - start)
            if text_replace not in stop_word:
                stop_free.append(text_replace)
        else:
            print(entity[2])
    stop_free = ' '.join(stop_free)
    return stop_free


def get_keyword(mesh_file, dict_file_name, synonyms_file):
    """
    Mesh keyword sorting
    :return:
    """
    synonyms_dict = {}
    # Mesh主题词内容
    mesh_words = list(pd.read_excel(mesh_file)['keyword'])
    for keyword in mesh_words:
        synonyms_dict[keyword.lower().strip()] = keyword.lower().strip()
    # 同义词表的内容
    data = pd.read_excel(synonyms_file)
    for index, row in data.iterrows():
        synonyms_dict[row['word'].lower().strip()] = row['delete'].lower().strip()
        synonyms_dict[row['delete'].lower().strip()] = row['delete'].lower().strip()

    # 关键词表的内容
    theme_words = pd.read_excel(dict_file_name)
    for column_name in list(theme_words.columns):
        word_list = list(theme_words[column_name])
        for word in word_list:
            if word is np.nan:
                continue
            else:
                word_one_list = word.lower().strip().split("#")
                word_key = word_one_list[0]
                other_word = []
                for word_one_one in word_one_list:
                    if word_one_one.find("/"):
                        other_word.append(word_one_one.replace("/", ' '))
                        other_word.append(word_one_one.replace("/", ' and '))
                word_one_list.extend(other_word)
                for word_value in word_one_list:
                    synonyms_dict[word_value.strip()] = word_key.strip()
    return synonyms_dict


def get_corpus_keyword(mesh_file, dict_file_name, synonyms_file, paper_file_name, trial_file_name, context_file,
                       context_word_count):
    """
    trial and paper data splicing, clean the data, and obtain separate data (ID, context)

    :param mesh_file: Mesh vocabulary path
    :param dict_file_name: Dictionary path
    :param synonyms_file:  Synonym table path
    :param paper_file_name: paper file
    :param trial_file_name: trial file
    :param context_file: Corpus file
    :param context_word_count: Corpus keyword frequency file
    :return:
    """
    # Synonym dictionary
    synonyms_dict = get_keyword(mesh_file, dict_file_name, synonyms_file)
    # Get dictionary content
    entity_dict = {'CONCEPT': list(synonyms_dict.keys())}
    patterns = wetlandEntityAnnotation.transform_dict_to_spacy(entity_dict)
    print("Corpus processing！")
    # Paper data
    column_dict = {'AB': 1, 'TI': 2, 'ID': 3}
    data = pd.read_excel(paper_file_name)
    data = data.fillna('')
    data['data'] = ''
    data['type'] = '论文'
    for column in list(column_dict.keys()):
        data[column].apply(lambda x: x.replace('\n   ', ' '))
        for i in range(column_dict[column]):
            data['data'] = data['data'] + ' ' + data[column]
    doc_clean = [clean_keyword(doc, patterns, synonyms_dict) for doc in list(data['data'])]
    # trial Data
    cinal_column_dict = {'Public title': 1, 'Scientific title': 2, '介入手段': 3}
    cinal_data = pd.read_excel(trial_file_name)
    cinal_data = cinal_data.fillna('')
    cinal_data['data'] = ''
    cinal_data['type'] = '试验'
    for cinal_column in list(cinal_column_dict.keys()):
        cinal_data[cinal_column].apply(lambda x: x.replace('\n', ' '))
        for i in range(cinal_column_dict[cinal_column]):
            cinal_data['data'] = cinal_data['data'] + ' ' + cinal_data[cinal_column]
    cinal_doc_clean = [clean_keyword(doc, patterns, synonyms_dict) for doc in list(cinal_data['data'])]
    # merge
    ids = list(data['UT'])
    ids.extend(list(cinal_data['TrialID']))
    types = list(data['type'])
    types.extend(list(cinal_data['type']))
    doc_clean.extend(cinal_doc_clean)
    data_all = pd.DataFrame(ids, columns=['id'])
    data_all['type'] = types
    data_all['context'] = doc_clean
    data_all.to_excel(context_file)
    # Matches per word
    from collections import Counter
    words = [i.split() for i in doc_clean]
    result_words = []
    for i in words:
        result_words.extend(i)
    word_count = Counter(result_words)
    result = []
    for key, value in word_count.items():
        result.append([key, value])
    result = pd.DataFrame(result, columns=['word', 'count(加权)'])
    result.sort_values(by=['count(加权)'], ascending=False, inplace=True)
    result.to_excel(context_word_count)
    print('The text is generated from the corpus')


# ---------------------Go to stop words etc. (text processing)---------------------------------
def clean_keyword_2(doc, patterns, synonyms_dict):
    """
    :param doc:
    :param patterns:
    :param synonyms_dict:
    :return:
    """
    # Prepare stop words
    from spacy.lang.en.stop_words import STOP_WORDS
    stop_words = list(STOP_WORDS)  # stopwords.words('english')
    stop_words.extend(['from', 'subject', 're', 'edu', 'use'])
    stop_words.extend(['treatment', 'vaccines', 'pneumonia', 'therapy', 'syndrome'])
    # Prepare common words
    common_file = 'common_words.xlsx'
    common = set(pd.read_excel(common_file)['words'])
    stop_words = set(stop_words) | common
    exclude = set(string.punctuation)
    exclude.add(' ')
    exclude.add('\n   ')
    exclude.add('   ')
    exclude.add('  ')

    doc = doc.replace('(', ' (')
    # Named entity recognition, synonym substitution
    entities = wetlandEntityAnnotation.spacy_ner_basedon_dict_2(doc, patterns)
    add = 0
    for entity in entities:
        start = entity[0]
        end = entity[1]
        if synonyms_dict.__contains__(entity[2]):
            result = synonyms_dict[entity[2]]
            text_replace = result.replace(' ', '_')
            doc = doc[:start + add] + text_replace + doc[end + add:]
            add = add + len(result) - (end - start)
    nlp = spacy.load('en_core_web_sm')
    doc_nlp = nlp(doc)
    normalized = [word.lemma_.lower() for word in doc_nlp]
    punc_free = [ch for ch in normalized if ch not in exclude]  # Depunctuation
    stop_free = [i for i in punc_free if i not in stop_words]
    stop_free = ' '.join(stop_free)
    return stop_free


def get_corpus_keyword_2(mesh_file, dict_file_name, synonyms_file, paper_file_name, trial_file_name, context_file,
                       context_word_count):
    path = 'D:/zyx-project/paper/python_code/src/data/'
    # Synonym dictionary
    synonyms_dict = get_keyword(mesh_file, dict_file_name, synonyms_file)
    data = pd.read_excel(path + 'synonyms.xlsx')
    for index, row in data.iterrows():
        synonyms_dict[row['word'].lower().strip()] = row['delete'].lower().strip()
        synonyms_dict[row['delete'].lower().strip()] = row['delete'].lower().strip()
    # Get dictionary content
    entity_dict = {'CONCEPT': list(synonyms_dict.keys())}
    patterns = wetlandEntityAnnotation.transform_dict_to_spacy(entity_dict)
    print("语料开始处理！")
    # Paper data
    column_dict = {'AB': 1, 'TI': 2, 'ID': 3}
    # column_dict = {'AB': 1, 'TI': 1, 'ID': 1}
    data = pd.read_excel(paper_file_name)
    data = data.fillna('')
    data['data'] = ''
    data['type'] = '论文'
    for column in list(column_dict.keys()):
        data[column].apply(lambda x: x.replace('\n   ', ' '))
        for i in range(column_dict[column]):
            data['data'] = data['data'] + ' ' + data[column]
    doc_clean = [clean_keyword_2(doc, patterns, synonyms_dict) for doc in list(data['data'])]

    # Trial Data
    cinal_column_dict = {'Public title': 1, 'Scientific title': 2, '介入手段': 3}
    cinal_data = pd.read_excel(trial_file_name)
    cinal_data = cinal_data.fillna('')
    cinal_data['data'] = ''
    cinal_data['type'] = '试验'
    for cinal_column in list(cinal_column_dict.keys()):
        cinal_data[cinal_column].apply(lambda x: x.replace('\n', ' '))
        for i in range(cinal_column_dict[cinal_column]):
            cinal_data['data'] = cinal_data['data'] + ' ' + cinal_data[cinal_column]
    cinal_doc_clean = [clean_keyword_2(doc, patterns, synonyms_dict) for doc in list(cinal_data['data'])]
    # merge
    ids = list(data['UT'])
    ids.extend(list(cinal_data['TrialID']))
    types = list(data['type'])
    types.extend(list(cinal_data['type']))
    doc_clean.extend(cinal_doc_clean)
    data_all = pd.DataFrame(ids, columns=['id'])
    data_all['type'] = types
    data_all['context'] = doc_clean
    data_all.to_excel(context_file)
    # Matches per word
    from collections import Counter
    words = [i.split() for i in doc_clean]
    result_words = []
    for i in words:
        result_words.extend(i)
    word_count = Counter(result_words)
    result = []
    for key, value in word_count.items():
        result.append([key, value])
    result = pd.DataFrame(result, columns=['word', 'count(加权)'])
    result.sort_values(by=['count(加权)'], ascending=False, inplace=True)
    result.to_excel(context_word_count)
    print('The text is generated from the corpus')


def get_topic_number(corpus_file_name, png_file):
    """
    Get the best theme, 6-30 traversal
    :param png_file:
    :param corpus_file_name:
    :return:
    """
    # TODO: 数据处理
    data = pd.read_excel(corpus_file_name)
    data['context'] = data['context'].apply(lambda x: x if x is not np.nan else '')
    doc_clean = [x.split() for x in list(data['context'])]
    dictionary = corpora.Dictionary(doc_clean)
    doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]
    results = []
    for i in range(6, 31, 1):
        print(i)
        # TODO: 模型训练
        Lda = gensim.models.ldamodel.LdaModel
        ldamodel = Lda(doc_term_matrix, num_topics=i, id2word=dictionary, random_state=4, iterations=1000)
        # TODO: 衡量模型
        cm_result = []
        for coherence in ['u_mass']:
            goodcm = CoherenceModel(model=ldamodel, corpus=doc_term_matrix, dictionary=dictionary, coherence=coherence)
            cm_result.append(goodcm.get_coherence())
        for coherence in ['c_v', 'c_uci', 'c_npmi']:
            goodcm = CoherenceModel(model=ldamodel, texts=doc_clean, dictionary=dictionary, coherence=coherence)
            cm_result.append(goodcm.get_coherence())
        print(cm_result)
        results.append(cm_result)
    results = pd.DataFrame(results, columns=['u_mass', 'c_v', 'c_uci', 'c_npmi'])
    plt.figure(figsize=(16, 8))
    plt.subplot(2, 2, 1)
    plt.plot(list(range(6, 31, 1)), list(results['u_mass']), label="u_mass", color="red", linewidth=1)
    plt.subplot(2, 2, 2)
    plt.plot(list(range(6, 31, 1)), list(results['c_v']), label="c_v", color="red", linewidth=1)
    plt.subplot(223)
    plt.plot(list(range(6, 31, 1)), list(results['c_uci']), label="c_uci", color="red", linewidth=1)
    plt.subplot(224)
    plt.plot(list(range(6, 31, 1)), list(results['c_npmi']), label="c_npmi", color="red", linewidth=1)
    plt.savefig(png_file)
    plt.show()


def format_topics_sentences(ldamodel, corpus, texts, data):
    # Init output
    sent_topics_df = pd.DataFrame()

    # Get main topic in each document
    for i, row in enumerate(ldamodel[corpus]):
        row = sorted(row, key=lambda x: (x[1]), reverse=True)
        # Get the Dominant topic, Perc Contribution and Keywords for each document
        for j, (topic_num, prop_topic) in enumerate(row):
            if j == 0:  # => dominant topic
                wp = ldamodel.show_topic(topic_num)
                topic_keywords = ", ".join([word for word, prop in wp])
                sent_topics_df = sent_topics_df.append(pd.Series([int(topic_num), round(prop_topic,4), topic_keywords]), ignore_index=True)
            else:
                break
    sent_topics_df.columns = ['Dominant_Topic', 'Perc_Contribution', 'Topic_Keywords']

    # Add original text to the end of the output
    contents = pd.Series(texts)
    sent_topics_df = pd.concat([sent_topics_df, contents], axis=1)
    sent_topics_df = pd.concat([sent_topics_df, data], axis=1)

    return sent_topics_df


def get_result_lda(corpus_file_name, paper_file_name, trial_file_name, result_paper_file, result_trail_file,
                   label_word_file, result_topic_file, most_relevant_file, topic_number, html_file):
    """
    Perform lda, get the result
    :param html_file:
    :param topic_number:
    :param most_relevant_file:
    :param result_topic_file:
    :param corpus_file_name: Corpus file
    :param paper_file_name: paper file
    :param trial_file_name: trial file
    :param result_paper_file: Tagged paper file
    :param result_trail_file: Tagged trial file
    :param label_word_file: Main word file
    :return:
    """
    # TODO: data processing
    data = pd.read_excel(corpus_file_name)
    data['context'] = data['context'].apply(lambda x: x if x is not np.nan else '')
    doc_clean = [x.split() for x in list(data['context'])]
    dictionary = corpora.Dictionary(doc_clean)
    doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]

    # TODO: 模型训练
    Lda = gensim.models.ldamodel.LdaModel
    ldamodel = Lda(doc_term_matrix, num_topics=topic_number, id2word=dictionary, random_state=4, iterations=1000)
    # TODO: Judgment tags, main keywords，Perc Contribution
    df_dominant_topic = format_topics_sentences(ldamodel, doc_term_matrix, doc_clean, data['id'])
    df_dominant_topic.columns = ['Dominant_Topic', 'Topic_Perc_Contrib', 'Keywords', 'Text', 'id']  # Show
    df_dominant_topic.to_excel(result_topic_file)

    labels = pd.DataFrame(list(df_dominant_topic['Dominant_Topic']), columns=['label'])
    paper_data = pd.read_excel(paper_file_name)
    trail_data = pd.read_excel(trial_file_name)
    paper_data['label'] = list(labels['label'])[:len(paper_data)]
    trail_data['label'] = list(labels['label'])[len(paper_data):]
    paper_data.to_excel(result_paper_file, index=False)
    trail_data.to_excel(result_trail_file, index=False)
    # TODO: Statistics of each category：
    print(labels['label'].value_counts())
    print('Statistics of the number of papers in each category')
    data['label'] = labels
    data1 = data[data['type'] == '论文']
    print(data1['label'].value_counts())
    print('Statistics of the number of trial in each  categories')
    data2 = data[data['type'] == '试验']
    print(data2['label'].value_counts())

    # TODO：Determine the top 10 words in the total frequency of each category
    s = ldamodel.print_topics(num_topics=topic_number, num_words=20)
    result_topic = []
    for doc_class, doc_t in s:
        doc_topics = doc_t.split('+')
        for doc_topic in doc_topics:
            result_topic.append([doc_class, doc_topic.split('*')[1].strip(), doc_topic.split('*')[0].strip()])
    result_topic = pd.DataFrame(result_topic, columns=['class', 'topic', 'score'])
    result_topic.to_excel(label_word_file, index=None)
    result_topic.to_excel(label_word_file, index=False)
    # TODO: Determine the most similar corpus (corpus, ID)
    sent_topics_sorteddf_mallet = pd.DataFrame()
    sent_topics_outdf_grpd = df_dominant_topic.groupby('Dominant_Topic')
    for i, grp in sent_topics_outdf_grpd:
        sent_topics_sorteddf_mallet = pd.concat([sent_topics_sorteddf_mallet,
                                                 grp.sort_values(['Topic_Perc_Contrib'], ascending=[0]).head(10)],
                                                axis=0)  # Reset Index
    sent_topics_sorteddf_mallet.reset_index(drop=True, inplace=True)  # Format
    sent_topics_sorteddf_mallet.columns = ['Topic_Num', "Topic_Perc_Contrib", "Keywords", "Text", 'id']  # Show
    sent_topics_sorteddf_mallet.head(10)
    sent_topics_sorteddf_mallet.to_excel(most_relevant_file, index=None)
    # TODO: Measurement model
    # cm_result = []
    # for coherence in ['u_mass']:
    #     goodcm = CoherenceModel(model=ldamodel, corpus=doc_term_matrix, dictionary=dictionary, coherence=coherence)
    #     cm_result.append(goodcm.get_coherence())
    # for coherence in ['c_v', 'c_uci', 'c_npmi']:
    #     goodcm = CoherenceModel(model=ldamodel, texts=doc_clean, dictionary=dictionary, coherence=coherence)
    #     cm_result.append(goodcm.get_coherence())
    # print(cm_result)
    vis = pyLDAvis.gensim.prepare(ldamodel, doc_term_matrix, dictionary)
    # pyLDAvis.show(vis)
    pyLDAvis.save_html(vis, html_file)

    print('Clustering complete！')


if __name__ == '__main__':
    path = 'D:/zyx-project/paper/python_paper/'
    mesh_file = path + "data_set/MESH主题词.xlsx"
    dict_file_name = path + "data_set/201104-临床关键词(论文、试验通用）.xlsx"
    synonyms_file = path + "data_set/synonyms.xlsx"
    paper_file_name = path + "data_set/paper_1231_filter.xlsx"
    trial_file_name = path + "data_set/trail_1231_filter_blind.xlsx"
    context_file = path + "data_set/层次聚类语料.xlsx"
    context_word_count = path + "data_set/层次聚类语料_词频.xlsx"
    # get_corpus_keyword_2(mesh_file, dict_file_name, synonyms_file, paper_file_name, trial_file_name, context_file,
    #                          context_word_count)
    png_file = 'lda_所有词.png'
    get_topic_number(context_file, png_file)