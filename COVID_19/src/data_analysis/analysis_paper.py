import pandas as pd
import pymysql
import numpy as np


def get_connection():
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='covid', charset='utf8')
    cursor = conn.cursor()
    return conn, cursor


def close_connection(conn, cursor):
    cursor.close()
    conn.close()


# ----------------------------------Institutional part----------------------------------
def get_org_number(paper_number_excel):
    """
    Get trials, papers, and total number of papers
    :param paper_number_excel:
    :param trail_number_excel:
    :param all_number_excel:
    :return:
    """
    conn, cursor = get_connection()
    # paper number
    sql_paper = '''
        SELECT country_clear , org_clear, count(DISTINCT paper_id) as num
        FROM paper_country
        GROUP BY country_clear, org_clear
        order by num desc
    '''
    cursor.execute(sql_paper)
    result_paper = cursor.fetchall()
    result_paper = pd.DataFrame(result_paper, columns=['country', 'org', 'number'])
    # storage
    result_paper.to_excel(paper_number_excel, index=None)
    close_connection(conn, cursor)


def get_h_index_org(org, country, cursor):
    sql_country = '''
    select  paper_id, TC
    from paper 
    where paper.paper_id in 
        (SELECT DISTINCT paper_id as id FROM paper_country where country_clear = '%s' and  org_clear = '%s')
    ''' % (country, org)

    cursor.execute(sql_country)
    data = cursor.fetchall()
    result = []
    for row in data:
        result.append([row[0], int(row[1])])
    paper_number = len(result)
    result = pd.DataFrame(result, columns=['id', 'TC'])
    for h in range(1, 100):
        number = len(result[result['TC'] >= h])
        if h > number:
            return (h - 1) / (paper_number ** 0.4)


def get_some_org_paper_info(org, country, country_count, sum_count, cursor):
    """
    Institution, country, number of publications, percentage, average citation frequency, h-index, number of cooperative papers, number of cooperative papers
    :param org:
    :param cursor:
    :param country: str, Country Name
    :param country_count int, Country's publication volume
    :param sum_count: int Total number of posts
    :return:
    """
    tc_sql = """
            select  avg(TC) as TC
            from paper 
            where paper.paper_id in 
                (SELECT DISTINCT paper_id as id FROM paper_country where country_clear = '%s' and  org_clear = '%s')
            """ % (country, org)
    co_sql = """
            select count(*) from (
            select count(paper_id)
            from paper_country
            where paper_id in 
                (select paper_id from paper_country where country_clear = '%s' and  org_clear = '%s')
            group by paper_id
            having count(DISTINCT org_clear) >=2 )a
            """ % (country, org)
    radio = np.around(country_count / sum_count, 4)  # Percentage
    # Average citation frequency
    cursor.execute(tc_sql)
    average_TC = np.around(cursor.fetchone()[0], 4)
    h_index = get_h_index_org(org, country, cursor)  # h-index
    # Number of collaborative papers
    cursor.execute(co_sql)
    co_count = cursor.fetchone()[0]
    co_radio = np.around(co_count / country_count, 4)  # Proportion of Cooperative Papers
    return [org, country, country_count, radio, average_TC, h_index, co_count, co_radio]


def get_org_top(paper_number_excel, paper_result_excel):
    """
    Get the top 10 forms
    1. Top 10 Papers--Institution, Country, Publication Volume, Percentage, Average Cited Frequency, h-index, Number of
    Cooperative Papers, Number of Cooperative Papers, Proportion of the Institution
    :param paper_number_excel: paper Documents issued
    :param paper_result_excel: paper top10 table
    :return:
    """
    conn, cursor = get_connection()

    # 获取并检查数据
    data_paper = pd.read_excel(paper_number_excel)
    paper_count = list(data_paper['number'])
    if paper_count[9] == paper_count[10]:
        print('The 11th-ranked institution and the 10th-ranked institution have the same amount of articles. '
              'Please manually determine how to analyze! ! !')
    # Get results
    paper_result = []
    for index, row in data_paper.head(11).iterrows():
        # Current national total
        sum_sql = "select count(distinct paper_id) from paper_country where country_clear = '%s'" % row['country']
        cursor.execute(sum_sql)
        sum_count = cursor.fetchone()[0]
        result_country = get_some_org_paper_info(row['org'], row['country'], row['number'], sum_count, cursor)
        paper_result.append(result_country)
    columns = ['机构', '国家', '发文量', '发文量占比', '平均被引频次', 'h_index', '合作论文数量', '合作论文数目占本机构发文量比值']
    paper_result = pd.DataFrame(paper_result, columns=columns)
    paper_result.to_excel(paper_result_excel, index=None)

    close_connection(conn, cursor)


def get_org_paper_month(org, country, cursor):
    """
    Get the number of papers of an institution in each month
    :param country:
    :param org:
    :param cursor:
    :return:
    """
    sql = """
        select a.publish_month, IFNULL(b.num,0) as num	from 
          (select distinct `number` as `publish_month` FROM `number` where `number` <= 12 and `number` >=1 ) a
        left join 
            (select `month`+0 as `publish_month`, count(*) as num  
            from paper where paper_id in 
                ( SELECT paper_id  FROM paper_country where `country_clear` = '%s' and org_clear = '%s') 
            group by `month` 
            ) b
        on a.`publish_month`= b.`publish_month` 
        order by a.publish_month asc
    """ % (country, org)
    cursor.execute(sql)
    result = cursor.fetchall()
    result_all = pd.DataFrame(result, columns=['month', 'number'])
    return list(result_all['number'])


def org_top10_month(paper_number_excel, paper_result_excel):
    """
    # Monthly publication volume of institutions
    # Country list
    # Query paper and return the month, statistics according to the month
    :param paper_number_excel:
    :param paper_result_excel:
    :return:
    """
    conn, cursor = get_connection()
    paper_top10_list = list(pd.read_excel(paper_number_excel).head(11)['org'])
    paper_top10_list_country = list(pd.read_excel(paper_number_excel).head(11)['country'])

    # 列名称
    columns = list(range(1, 13))
    columns = [str(i) for i in columns]
    columns = ['机构'] + columns
    # ---论文---
    paper_result = []
    for i in range(len(paper_top10_list)):
        result_country = get_org_paper_month(paper_top10_list[i], paper_top10_list_country[i], cursor)
        paper_result.append([paper_top10_list[i]] + result_country)
    paper_result = pd.DataFrame(paper_result, columns=columns)
    paper_result.to_excel(paper_result_excel, index=None)

    close_connection(conn, cursor)


def get_org_paper_intervention(org, country, label, cursor):
    """
    Get the number of papers in each category in a country
    :param org:
    :param label:
    :param country:
    :param cursor:
    :return:
    """
    sql = """
    	 select c.publish_month, IFNULL(SUM(num),0) as num	from (
         select aa.publish_month, IFNULL(bb.num,0) as num	from 
            (select TRIM(top_ipc) as `publish_month`, count(*) as `number` from 
                    (SELECT substring_index(substring_index(sub_ipc,',',`help_topic_id`+1),',',-1) as `top_ipc` 
                    FROM mysql.`help_topic` , (select topic as sub_ipc 
                    from `paper` ) as a 
                    where  
                         mysql.help_topic.help_topic_id < (LENGTH(sub_ipc)-LENGTH(REPLACE(sub_ipc,',',''))+1) ) as b
                     where b.top_ipc is not NULL and b.top_ipc != ''
                     GROUP BY TRIM(top_ipc)
                     order by TRIM(top_ipc) desc 
                ) aa
        left join 
                (select topic as `publish_month`, count(*) as num  from paper where paper_id in 
                        ( SELECT paper_id  FROM paper_country where `country_clear` = '%s' and org_clear = '%s') group by `publish_month` 
                ) bb
        on FIND_IN_SET(aa.`publish_month`, bb.`publish_month` )
            order by aa.publish_month
            ) c 
        group by c.publish_month
        order by c.publish_month 
    """ % (country, org)
    cursor.execute(sql)
    result = cursor.fetchall()
    result_all = pd.DataFrame(result, columns=['label', 'number'])
    return list(result_all['number'])


def org_top10_intervention(paper_number_excel, paper_result_excel, label):
    """
    :param label:
    :param paper_number_excel: Used to get the top 10 institutions
    :param paper_result_excel:
    :return:
    """
    conn, cursor = get_connection()
    paper_top10_list = list(pd.read_excel(paper_number_excel).head(11)['org'])
    paper_top10_list_country = list(pd.read_excel(paper_number_excel).head(11)['country'])
    # Column name
    sql = """
    select TRIM(top_ipc) as `keyword plus` from 
    (SELECT substring_index(substring_index(sub_ipc,',',`help_topic_id`+1),',',-1) as `top_ipc` 
    FROM mysql.`help_topic` , (select topic as sub_ipc 
    from `paper` ) as a 
    where  
       mysql.help_topic.help_topic_id < (LENGTH(sub_ipc)-LENGTH(REPLACE(sub_ipc,',',''))+1) ) as b
     where b.top_ipc is not NULL and b.top_ipc != ''
     GROUP BY TRIM(top_ipc)
     order by TRIM(top_ipc) 
    """
    cursor.execute(sql)
    columns = cursor.fetchall()
    columns = pd.DataFrame(columns, columns=['label'])
    columns = ['机构'] + list(columns['label'])
    # paper
    paper_result = []
    for i in range(len(paper_top10_list)):
        result_country = get_org_paper_intervention(paper_top10_list[i], paper_top10_list_country[i], label, cursor)
        paper_result.append([paper_top10_list[i]] + result_country)
    paper_result = pd.DataFrame(paper_result, columns=columns)
    paper_result.to_excel(paper_result_excel, index=None)
    close_connection(conn, cursor)


def get_org_paper_type(org, country, label, cursor):
    """
    Get the amount of papers in each category of an institution
    :param org:
    :param label:
    :param country:
    :param cursor:
    :return:
    """
    sql = """
         select a.publish_month, IFNULL(b.num,0) as num	from 
            (select distinct %s as `publish_month` FROM `paper` ) a
        left join 
                (select %s as `publish_month`, count(*) as num  from paper where paper_id in 
                        ( SELECT paper_id  FROM paper_country where `country_clear` = '%s' and org_clear = '%s') 
                 group by `publish_month` 
                ) b
        on a.`publish_month`= b.`publish_month` 
        order by a.publish_month 
    """ % (label, label, country, org)
    cursor.execute(sql)
    result = cursor.fetchall()
    result_all = pd.DataFrame(result, columns=['label', 'number'])
    return list(result_all['number'])


def org_top10_type(paper_number_excel, paper_result_excel, label):
    """
    # The amount of documents issued by each category 论文
    :param label:
    :param paper_number_excel: Used to get the top 10 institutions
    :param paper_result_excel:
    :return:
    """
    conn, cursor = get_connection()
    paper_top10_list = list(pd.read_excel(paper_number_excel).head(11)['org'])
    paper_top10_list_country = list(pd.read_excel(paper_number_excel).head(11)['country'])
    # Column name
    sql = 'select distinct %s as `publish_month` FROM `paper` order by %s ' % (label, label)
    cursor.execute(sql)
    columns = cursor.fetchall()
    columns = pd.DataFrame(columns, columns=['label'])
    columns = ['机构'] + list(columns['label'])
    # paper
    paper_result = []
    for i in range(len(paper_top10_list)):
        result_country = get_org_paper_type(paper_top10_list[i], paper_top10_list_country[i], label, cursor)
        paper_result.append([paper_top10_list[i]] + result_country)
    paper_result = pd.DataFrame(paper_result, columns=columns)
    paper_result.to_excel(paper_result_excel, index=None)
    close_connection(conn, cursor)


# ----------------------------------Journal section----------------------------------
def get_publish_number(paper_number_excel):
    """
    Get the number of articles published by the journal    :param paper_number_excel:
    :param trail_number_excel:
    :param all_number_excel:
    :return:
    """
    conn, cursor = get_connection()
    # ----Paper volume----
    # paper number
    sql_paper = '''
        select SO, count(distinct paper_id) as num from paper group by SO order by num desc
    '''
    cursor.execute(sql_paper)
    result_paper = cursor.fetchall()
    result_paper = pd.DataFrame(result_paper, columns=['SO', 'number'])
    # storage
    result_paper.to_excel(paper_number_excel, index=None)
    close_connection(conn, cursor)


def get_publish_paper_month(so, cursor):
    """
    Get the number of papers in each month of the journal
    :param so:
    :param cursor:
    :return:
    """
    sql = """
        select a.publish_month, IFNULL(b.num,0) as num	from 
          (select distinct `number` as `publish_month` FROM `number` where `number` <= 12 and `number` >=1 ) a
        left join 
            (select `month`+0 as `publish_month`, count(*) as num  
            from paper where SO = '%s' 
            group by `month` 
            ) b
        on a.`publish_month`= b.`publish_month` 
        order by a.publish_month asc

    """ % so
    cursor.execute(sql)
    result = cursor.fetchall()
    result_all = pd.DataFrame(result, columns=['month', 'number'])
    return list(result_all['number'])


def publish_top10_month(paper_number_excel, paper_result_excel):
    """
    # Monthly publication volume of journals
    :param paper_number_excel:
    :param paper_result_excel:
    :return:
    """
    conn, cursor = get_connection()
    data = pd.read_excel(paper_number_excel)
    paper_count = list(data['number'])
    if paper_count[9] == paper_count[10]:
        print('The 11th-ranked journal and the 10th-ranked journal have the same amount of published articles. '
              'Please manually determine how to analyze! ! !')

    paper_top10_list = list(data.head(10)['SO'])

    # Column name
    columns = list(range(1, 13))
    columns = [str(i) for i in columns]
    columns = ['期刊'] + columns
    # ---paper---
    paper_result = []
    for i in range(len(paper_top10_list)):
        result_country = get_publish_paper_month(paper_top10_list[i], cursor)
        paper_result.append([paper_top10_list[i]] + result_country)
    paper_result = pd.DataFrame(paper_result, columns=columns)
    paper_result.to_excel(paper_result_excel, index=None)

    close_connection(conn, cursor)


# ----------------------------------学科部分----------------------------------
def get_wc_number(paper_number_excel):
    """
    获取 论文  的发文量
    :param paper_number_excel:
    :return:
    """
    conn, cursor = get_connection()
    # ----试验，论文发文量----
    # 论文数目
    sql_paper = '''
        select wc, count(distinct paper_id) as num from paper_wc group by wc order by num desc
    '''
    cursor.execute(sql_paper)
    result_paper = cursor.fetchall()
    result_paper = pd.DataFrame(result_paper, columns=['WC', 'number'])
    # 存储
    result_paper.to_excel(paper_number_excel, index=None)
    close_connection(conn, cursor)


def get_wc_paper_month(wc, cursor):
    """
    获取某机构各个月份论文量
    :param wc:
    :param cursor:
    :return:
    """
    sql = """
        select a.publish_month, IFNULL(b.num,0) as num	from 
          (select distinct `number` as `publish_month` FROM `number` where `number` <= 12 and `number` >=1 ) a
        left join 
            (select `month`+0 as `publish_month`, count(*) as num  
            from paper where paper_id in 
                ( SELECT paper_id  FROM paper_wc where `wc` = '%s') 
            group by `month` 
            ) b
        on a.`publish_month`= b.`publish_month` 
        order by a.publish_month asc
    """ % wc
    cursor.execute(sql)
    result = cursor.fetchall()
    result_all = pd.DataFrame(result, columns=['month', 'number'])
    return list(result_all['number'])


def wc_top10_month(paper_number_excel, paper_result_excel):
    """
    # 学科每月发文量
    # 查询paper 并 返回 月份， 按照月份统计
    :param paper_number_excel:
    :param paper_result_excel:
    :return:
    """
    conn, cursor = get_connection()

    data = pd.read_excel(paper_number_excel)
    paper_count = list(data['number'])
    if paper_count[9] == paper_count[10]:
        print('paper发文量排名11的学科和排名10的学科发文量相同，请人工确定如何进行分析！！！')

    paper_top10_list = list(data.head(10)['WC'])
    # 列名称
    columns = list(range(1, 13))
    columns = [str(i) for i in columns]
    columns = ['学科'] + columns
    # ---论文---
    paper_result = []
    for i in range(len(paper_top10_list)):
        result_country = get_wc_paper_month(paper_top10_list[i], cursor)
        paper_result.append([paper_top10_list[i]] + result_country)
    paper_result = pd.DataFrame(paper_result, columns=columns)
    paper_result.to_excel(paper_result_excel, index=None)

    close_connection(conn, cursor)


def wc_some_country_number(wc, country_list, cursor):
    """
    某个国家某个学科的数目
    :param wc:
    :param country_list:
    :param cursor:
    :return:
    """
    sql = """
            select count(distinct paper_id)
            from paper 
             where paper_id in  (SELECT paper_id  FROM paper_wc where `wc` = '%s') 
             and paper_id in  (SELECT paper_id  FROM paper_country where `country_clear` = '%s') 
        """
    eu_sql = """
            select count(distinct paper_id)
            from paper 
             where paper_id in  (SELECT paper_id  FROM paper_wc where `wc` = '%s') 
             and paper_id in  (SELECT paper_id  FROM paper_country where is_eu =1) 
    """
    non_eu_sql = """
            select count(distinct paper_id)
            from paper 
             where paper_id in  (SELECT paper_id  FROM paper_wc where `wc` = '%s') 
             and paper_id in  (SELECT paper_id  FROM paper_country where is_eu =0) 
    """
    results = []
    for country in country_list:
        country_sql = sql % (wc, country)
        if country == 'europe':
            country_sql = eu_sql % wc
        elif country == 'non-europe':
            country_sql = non_eu_sql % wc
        cursor.execute(country_sql)
        result = cursor.fetchone()[0]
        results.append(result)
    return results


def wc_top10_country(paper_number_excel, country_number_excel, paper_result_excel):
    """
    # 学科 某些国家的发文量
    # 国家列表
    # 查询paper 并 返回 月份， 按照月份统计
    :param country_number_excel: 从这个文件里获取国家
    :param paper_number_excel: 获取期刊
    :param paper_result_excel:
    :return:
    """
    conn, cursor = get_connection()
    paper_top10_list = list(pd.read_excel(paper_number_excel).head(10)['WC'])
    data = pd.read_excel(country_number_excel)
    data = data[~ (data['country'] == 'europe')]
    data = data[~ (data['country'] == 'non-europe')]
    country_list = list(data.head(10)['country'])

    # 列名称
    columns = ['学科'] + country_list
    # ---论文---
    paper_result = []
    for i in range(len(paper_top10_list)):
        result_country = wc_some_country_number(paper_top10_list[i], country_list, cursor)
        paper_result.append([paper_top10_list[i]] + result_country)
    paper_result = pd.DataFrame(paper_result, columns=columns)
    paper_result.to_excel(paper_result_excel, index=None)

    close_connection(conn, cursor)


def get_matrix(sql, cursor, file_name):
    """
    根据sql 获得矩阵
    :param sql:
    :param cursor:
    :param file_name:
    :return:
    """
    cursor.execute(sql)
    rows = cursor.fetchall()
    data = pd.DataFrame(rows, columns=['detail_id', 'name'])

    word_list = list(set(data['name'].values))
    detail_id_list = list(set(data['detail_id'].values))

    word_matrix = np.zeros((len(word_list), len(word_list)))
    for detail_id in detail_id_list:
        data_with_detail_id = data[data['detail_id'] == detail_id]['name'].values.tolist()
        for i in data_with_detail_id:
            for j in data_with_detail_id:
                i_index = word_list.index(i)
                j_index = word_list.index(j)
                if i == j:
                    word_matrix[i_index][j_index] = word_matrix[i_index][j_index] + 1
                else:
                    word_matrix[i_index][j_index] = word_matrix[i_index][j_index] + 1
                    word_matrix[j_index][i_index] = word_matrix[j_index][i_index] + 1

    word_df = pd.DataFrame(word_matrix, columns=word_list, index=word_list)
    word_df.to_excel(file_name)


def get_node(df_file_name, node_file_name, node_limit):
    """
    获得点集
    :param node_limit: 点的大小的限制
    :param df_file_name: 共现矩阵文件
    :param node_file_name: 结果文件
    :return:
    """
    word_df = pd.read_excel(df_file_name, index_col=0)
    word_list = list(word_df.columns)

    word_matrix = word_df.iloc[:, :].values
    results = []
    for node in word_list:
        i = word_list.index(node)
        if int(word_matrix[i][i]) > 0 and int(word_matrix[i][i]) >= node_limit:
            results.append([node, node, word_matrix[i][i]])
    results_df = pd.DataFrame(results, columns=['id', 'label', 'number'])
    results_df.to_excel(node_file_name, index=None)


def get_triple_number(df_file_name, node_file_name, triple_file_name, triple_limit):
    """
    获得边集
    :param triple_limit: 边大小的限制
    :param df_file_name: 共现矩阵文件
    :param node_file_name: 点集文件
    :param triple_file_name:
    :return:
    """
    word_df = pd.read_excel(df_file_name, index_col=0)
    word_list = list(pd.read_excel(node_file_name)['label'])

    word_matrix = word_df.iloc[:, :].values  # cosine_similarity(word_df)
    results = []
    for i in range((len(word_list))):
        for j in range(i+1, len(word_list)):
            ii = word_list.index(word_list[i])
            jj = word_list.index(word_list[j])
            if word_matrix[ii][jj] > 0 and word_matrix[ii][jj] >= triple_limit and ii != jj:
                results.append([word_list[i], word_list[j], abs(word_matrix[ii][jj])])
    results_df = pd.DataFrame(results, columns=['source', 'target', 'Weight'])
    results_df.to_excel(triple_file_name, index=None)


def wc_network(paper_number_excel, df_paper_file_name, df_top10_file_name, node_all_file_name, triple_all_file_name,
               node_limit, triple_limit):
    # 获取前10，然后看共现次数
    conn, cursor = get_connection()
    # 论文
    paper_sql = """
                    select paper_id, wc 
                    from paper_wc 
                    group by paper_id, wc 
                    order by paper_id
                """
    get_matrix(paper_sql, cursor, df_paper_file_name)
    data = pd.read_excel(df_paper_file_name, index_col=0)
    top10_list = list(pd.read_excel(paper_number_excel).head(20)['WC'])
    data = data[top10_list]
    data = data.loc[top10_list]
    data.to_excel(df_top10_file_name)
    get_node(df_paper_file_name, node_all_file_name, node_limit)
    get_triple_number(df_paper_file_name, node_all_file_name, triple_all_file_name, triple_limit)
    close_connection(conn, cursor)


# ----------------------------------资助机构部分----------------------------------
# def get_fu_number(paper_number_excel):
#     """
#     获取 资助机构的发文量
#     :param paper_number_excel:
#     :return:
#     """
#     conn, cursor = get_connection()
#     # ----论文发文量----
#     # 论文数目
#     sql_paper = '''
#         select financial_name, count(distinct paper_id) as num from paper_financial group by financial_name order by num desc
#     '''
#     cursor.execute(sql_paper)
#     result_paper = cursor.fetchall()
#     result_paper = pd.DataFrame(result_paper, columns=['FU', 'number'])
#     # 存储
#     result_paper.to_excel(paper_number_excel, index=None)
#     close_connection(conn, cursor)
#
#
# def get_fu_paper_type(fu, label, cursor):
#     """
#     获取某资助机构的 各个类别论文量
#     :param label:
#     :param fu:
#     :param cursor:
#     :return:
#     """
#     sql = """
#          select a.publish_month, IFNULL(b.num,0) as num	from
#             (select distinct %s as `publish_month` FROM `paper` ) a
#         left join
#                 (select %s as `publish_month`, count(*) as num  from paper where paper_id in
#                         ( SELECT paper_id  FROM paper_financial where `financial_name` = '%s') group by `publish_month`
#                 ) b
#         on a.`publish_month`= b.`publish_month`
#         order by a.publish_month
#     """ % (label, label, fu)
#     cursor.execute(sql)
#     result = cursor.fetchall()
#     result_all = pd.DataFrame(result, columns=['label', 'number'])
#     return list(result_all['number'])
#
#
# def fu_top10_type(paper_number_excel, paper_result_excel, label):
#     """
#     # 资助机构国家每个类别的发文量
#     # 查询paper 并 返回 月份， 按照月份统计
#     :param label: 标签
#     :param paper_number_excel: 用来获取前10资助机构
#     :param paper_result_excel:
#     :return:
#     """
#     conn, cursor = get_connection()
#     paper_top10_list = list(pd.read_excel(paper_number_excel).head(10)['FU'])
#     # 列名称
#     sql = 'select distinct %s as `publish_month` FROM `paper` order by %s ' % (label, label)
#     cursor.execute(sql)
#     columns = cursor.fetchall()
#     columns = pd.DataFrame(columns, columns=['label'])
#     columns = ['国家'] + list(columns['label'])
#     # 论文
#     paper_result = []
#     for country in paper_top10_list:
#         result_country = get_fu_paper_type(country, label, cursor)
#         paper_result.append([country] + result_country)
#     paper_result = pd.DataFrame(paper_result, columns=columns)
#     paper_result.to_excel(paper_result_excel, index=None)
#     close_connection(conn, cursor)
#
#
# def get_fu_paper_intervention(fu, label, cursor):
#     """
#     获取某资助机构的 各个类别论文量
#     :param label:
#     :param fu:
#     :param cursor:
#     :return:
#     """
#     sql = """
#         select c.publish_month, IFNULL(SUM(num),0) as num	from (
#             select aa.publish_month, IFNULL(bb.num,0) as num	from
#             (select TRIM(top_ipc) as `publish_month`, count(*) as `number` from
#                     (SELECT substring_index(substring_index(sub_ipc,',',`help_topic_id`+1),',',-1) as `top_ipc`
#                     FROM mysql.`help_topic` , (select topic as sub_ipc
#                     from `paper` ) as a
#                     where
#                          mysql.help_topic.help_topic_id < (LENGTH(sub_ipc)-LENGTH(REPLACE(sub_ipc,',',''))+1) ) as b
#                      where b.top_ipc is not NULL and b.top_ipc != ''
#                      GROUP BY TRIM(top_ipc)
#                      order by TRIM(top_ipc) desc
#                 ) aa
#         left join
#                 (select topic as `publish_month`, count(*) as num  from paper where paper_id in
#                         ( SELECT paper_id  FROM paper_financial where `financial_name` = '%s') group by `publish_month`
#                 ) bb
#         on FIND_IN_SET(aa.`publish_month`, bb.`publish_month` )
#         order by aa.publish_month
#         ) c
#         group by c.publish_month
#         order by c.publish_month
#     """ % fu
#     cursor.execute(sql)
#     result = cursor.fetchall()
#     result_all = pd.DataFrame(result, columns=['label', 'number'])
#     return list(result_all['number'])
#
#
# def fu_top10_intervention(paper_number_excel, paper_result_excel, label):
#     """
#     # 资助机构国家每个类别的发文量
#     # 查询paper 并 返回 月份， 按照月份统计
#     :param label: 标签
#     :param paper_number_excel: 用来获取前10资助机构
#     :param paper_result_excel:
#     :return:
#     """
#     conn, cursor = get_connection()
#     paper_top10_list = list(pd.read_excel(paper_number_excel).head(10)['FU'])
#     # 列名称
#     sql = """
#     select TRIM(top_ipc) as `keyword plus`  from
#     (SELECT substring_index(substring_index(sub_ipc,',',`help_topic_id`+1),',',-1) as `top_ipc`
#     FROM mysql.`help_topic` , (select topic as sub_ipc
#     from `paper` ) as a
#     where
#        mysql.help_topic.help_topic_id < (LENGTH(sub_ipc)-LENGTH(REPLACE(sub_ipc,',',''))+1) ) as b
#      where b.top_ipc is not NULL and b.top_ipc != ''
#      GROUP BY TRIM(top_ipc)
#      order by TRIM(top_ipc)
#     """
#     cursor.execute(sql)
#     columns = cursor.fetchall()
#     columns = pd.DataFrame(columns, columns=['label'])
#     columns = ['国家'] + list(columns['label'])
#     # 论文
#     paper_result = []
#     for country in paper_top10_list:
#         result_country = get_fu_paper_intervention(country, label, cursor)
#         paper_result.append([country] + result_country)
#     paper_result = pd.DataFrame(paper_result, columns=columns)
#     paper_result.to_excel(paper_result_excel, index=None)
#     close_connection(conn, cursor)

