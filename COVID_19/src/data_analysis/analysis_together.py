"""
是一起分析的部分，放在这个文件里。
"""
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


def get_over_all(patient_data_file, to_file_name):
    """
    # 获取每月论文数目，每月发文量，成果数目和感染人数
    :param patient_data_file: 每月新增患者excel
    :param to_file_name: 输出的excel--每月成果数目
    :return:
    """
    conn, cursor = get_connection()
    # 论文数目
    sql_paper = 'SELECT `month`,count(*) FROM paper where `month` is not null group by `month` order by `month`+0 asc'
    cursor.execute(sql_paper)
    result_paper = cursor.fetchall()
    result_paper = pd.DataFrame(result_paper, columns=['month', 'paper_number'])
    # 试验数目
    sql_trail = 'SELECT `month`+0,count(*) FROM trail where `month` is not null group by `month` order by `month`+0 asc'
    cursor.execute(sql_trail)
    result_trail = cursor.fetchall()
    result_trail = pd.DataFrame(result_trail, columns=['month', 'trail_number'])
    result_trail['month'] = result_trail['month'].astype(int).astype(str)
    # 感染人数和增长率
    patient_data = pd.read_excel(patient_data_file)
    patient_data = patient_data[['month', '新增量', '增长率']]
    patient_data['month'] = patient_data['month'].astype(str)
    # 合成一个文件
    result = pd.merge(result_paper, result_trail, on='month')
    result = pd.merge(result, patient_data, on='month')
    # 修改月份映射
    month_json = {'1': 'Jan.', '2': 'Feb.', '3': 'Mar.', '4': 'Apr.', '5': 'May', '6': 'June', '7': 'July', '8': 'Aug.',
                  '9': 'Sept.', '10': 'Oct.', '11': 'Nov.', '12': 'Dec.'}
    result['month'] = result['month'].apply(lambda x: month_json[x])
    result.to_excel(to_file_name, index=None)
    close_connection(conn, cursor)


# ----------------------------------国家部分----------------------------------
def get_country_number(paper_number_excel, trail_number_excel, all_number_excel):
    """
    获取试验，论文和总的的发文量
    :param paper_number_excel:
    :param trail_number_excel:
    :param all_number_excel:
    :return:
    """
    conn, cursor = get_connection()
    # ----试验，论文发文量----
    # 论文数目
    sql_paper = '''
        select country_clear, num from (
        SELECT country_clear , count(DISTINCT paper_id) as num
        FROM paper_country
        GROUP BY country_clear
        UNION ALL
        SELECT 'europe' as country_clear, count(DISTINCT paper_id) as num
        FROM paper_country
        where is_eu = 1
        UNION ALL
        SELECT 'non-europe' as country_clear, count(DISTINCT paper_id) as num
        FROM paper_country
        where is_eu = 0
        ) a
        order by num desc
    '''
    cursor.execute(sql_paper)
    result_paper = cursor.fetchall()
    result_paper = pd.DataFrame(result_paper, columns=['country', 'number'])
    # 试验数目
    sql_trail = '''
        select country, num from (
        SELECT country , count(DISTINCT paper_id) as num
        FROM trial_country
        GROUP BY country
        UNION ALL
        SELECT 'europe' as country, count(DISTINCT paper_id) as num
        FROM trial_country
        where is_eu = 1
        UNION ALL
        SELECT 'non-europe' as country, count(DISTINCT paper_id) as num
        FROM trial_country
        where is_eu = 0) a
        order by num desc
    '''
    cursor.execute(sql_trail)
    result_trail = cursor.fetchall()
    result_trail = pd.DataFrame(result_trail, columns=['country', 'number'])
    # 总数目
    sql_all = '''
            select country_clear, sum(num) from (
                SELECT country_clear , count(DISTINCT paper_id) as num
                FROM paper_country
                GROUP BY country_clear
                UNION ALL
                SELECT 'europe' as country_clear, count(DISTINCT paper_id) as num
                FROM paper_country
                where is_eu = 1
                UNION ALL
                SELECT 'non-europe' as country_clear, count(DISTINCT paper_id) as num
                FROM paper_country
                where is_eu = 0
                UNION ALL
                SELECT country as country_clear, count(DISTINCT paper_id) as num
                FROM trial_country
                GROUP BY country
                UNION ALL
                SELECT 'europe' as country_clear, count(DISTINCT paper_id) as num
                FROM trial_country
                where is_eu = 1 
                UNION ALL
                SELECT 'non-europe' as country_clear, count(DISTINCT paper_id) as num
                FROM trial_country
                where is_eu = 0 )a
            GROUP BY country_clear
            order by sum(num) desc
        '''
    cursor.execute(sql_all)
    result_all = cursor.fetchall()
    result_all = pd.DataFrame(result_all, columns=['country', 'number'])
    # 存储
    result_paper.to_excel(paper_number_excel, index=None)
    result_trail.to_excel(trail_number_excel, index=None)
    result_all.to_excel(all_number_excel, index=None)
    close_connection(conn, cursor)


def get_h_index_country(country, cursor):
    sql_country = '''
    select  paper_id, TC
    from paper 
    where paper.paper_id in (SELECT DISTINCT paper_id as id FROM paper_country where country_clear = '%s' )
    ''' % country
    if country == 'europe':
        sql_country = '''
                select  paper_id, TC
                from paper 
                where paper.paper_id in (SELECT DISTINCT paper_id as id FROM paper_country where is_eu = 1 ) 
                '''
    if country == 'non-europe':
        sql_country = '''
                select  paper_id, TC
                from paper 
                where paper.paper_id in (SELECT DISTINCT paper_id as id FROM paper_country where is_eu = 0 ) 
                '''
    cursor.execute(sql_country)
    data = cursor.fetchall()
    result = []
    for row in data:
        result.append([row[0], int(row[1])])
    paper_number = len(result)
    result = pd.DataFrame(result, columns=['id', 'TC'])
    for h in range(1, 500):
        number = len(result[result['TC'] >= h])
        if h > number:
            return (h - 1) / (paper_number ** 0.4)


def get_some_country_paper_info(country, country_count, sum_count, cursor):
    """
    获得某个国家的 发文量，占比，平均被引频次，h-index, 合作论文数目, 合作论文数目本国占比
    :param cursor:
    :param country: str, 国家名称
    :param country_count int, 国家的发文量
    :param sum_count: int 发文量总数
    :return:
    """
    tc_sql = """
            select  avg(TC) as TC
            from paper 
            where paper.paper_id in (SELECT DISTINCT paper_id as id FROM paper_country where country_clear = '%s' )
            """ % country
    co_sql = """
            select count(*) from (
            select count(paper_id)
            from paper_country
            where paper_id in (select paper_id from paper_country where country_clear = '%s')
            group by paper_id
            having count(DISTINCT country_clear) >=2 )a
            """ % country
    if country == 'europe':
        tc_sql = """
                    select  avg(TC) as TC
                    from paper 
                    where paper.paper_id in (SELECT DISTINCT paper_id as id FROM paper_country where is_eu = 1 )
                 """
        co_sql = """
                    select count(*) from (
                        select count(paper_id)
                        from paper_country
                        where paper_id in (select paper_id from paper_country where is_eu = 1)
                        and is_eu != 1
                        group by paper_id ) a
                 """
    if country == 'non-europe':
        tc_sql = """
                       select  avg(TC) as TC
                       from paper 
                       where paper.paper_id in (SELECT DISTINCT paper_id as id FROM paper_country where is_eu = 0 )
                    """
        co_sql = """
                       select count(*) from (
                           select count(paper_id)
                           from paper_country
                           where paper_id in (select paper_id from paper_country where is_eu = 0)
                           and is_eu != 0
                           group by paper_id ) a
                    """
    radio = np.around(country_count / sum_count, 4)  # 占比
    # 平均被引频次
    cursor.execute(tc_sql)
    average_TC = np.around(cursor.fetchone()[0], 4)
    h_index = get_h_index_country(country, cursor)  # h-index
    # 合作论文数目
    cursor.execute(co_sql)
    co_count = cursor.fetchone()[0]
    co_radio = np.around(co_count / country_count, 4)  # 合作论文占比
    return [country, country_count, radio, average_TC, h_index, co_count, co_radio]


def get_some_country_trail_info(country, country_count, sum_count, cursor):
    """
    获得某个国家的 试验数量，试验占比，合作试验数目, 合作试验占比
    :param cursor:
    :param country: str, 国家名称
    :param country_count int, 国家的发文量
    :param sum_count: int 发文量总数
    :return:
    """
    co_sql = """
            select count(*) from (
            select count(paper_id)
            from trial_country
            where paper_id in (select paper_id from trial_country where country = '%s')
            group by paper_id
            having count(DISTINCT country) >=2 )a
            """ % country
    if country == 'europe':
        co_sql = """
                    select count(*) from (
                    select count(paper_id)
                    from trial_country
                    where paper_id in (select paper_id from trial_country where is_eu = 1)
                    and is_eu != 1
                    group by paper_id ) a
                 """
    if country == 'non-europe':
        co_sql = """
                    select count(*) from (
                    select count(paper_id)
                    from trial_country
                    where paper_id in (select paper_id from trial_country where is_eu = 0)
                    and is_eu != 0
                    group by paper_id ) a
                 """
    radio = np.around(country_count / sum_count, 4)  # 占比
    # 合作试验数目
    cursor.execute(co_sql)
    co_count = cursor.fetchone()[0]
    co_radio = np.around(co_count / country_count, 4)  # 合作试验占比
    return [country, country_count, radio, co_count, co_radio]


def get_some_country_all_info(country, country_count, sum_count, cursor):
    """
    获得某个国家的 论文和试验 数量，占比，合作数目, 合作占比
    :param cursor:
    :param country: str, 国家名称
    :param country_count int, 国家的发文量
    :param sum_count: int 成果量总数
    :return:
    """
    co_sql = """
            select sum(num) from (
            select count(*) as num from (
            select count(paper_id)
            from paper_country
            where paper_id in (select paper_id from paper_country where country_clear = '%s')
            group by paper_id
            having count(DISTINCT country_clear) >=2 )a1
            union
            select count(*) as num from (
            select count(paper_id)
            from trial_country
            where paper_id in (select paper_id from trial_country where country = '%s')
            group by paper_id
            having count(DISTINCT country) >=2 )a2 ) a
            """ % (country, country)
    if country == 'europe':
        co_sql = """
                select sum(num) from (
                select count(*) as num from (
                    select count(paper_id)
                    from paper_country
                    where paper_id in (select paper_id from paper_country where is_eu = 1)
                    and is_eu != 1
                    group by paper_id ) a2
                union
                select count(*) as num from (
                    select count(paper_id)
                    from trial_country
                    where paper_id in (select paper_id from trial_country where is_eu = 1)
                    and is_eu != 1
                    group by paper_id ) a2 )a
                 """
    if country == 'non-europe':
        co_sql = """
                select sum(num) from (
                select count(*) as num from (
                    select count(paper_id)
                    from paper_country
                    where paper_id in (select paper_id from paper_country where is_eu = 0)
                    and is_eu != 0
                    group by paper_id ) a2
                union
                select count(*) as num from (
                    select count(paper_id)
                    from trial_country
                    where paper_id in (select paper_id from trial_country where is_eu = 0)
                    and is_eu != 0
                    group by paper_id ) a2 )a
                 """
    radio = np.around(float(country_count) / float(sum_count), 4)  # 占比
    # 合作试验数目
    cursor.execute(co_sql)
    co_count = cursor.fetchone()[0]
    co_radio = np.around(float(co_count) / float(country_count), 4)  # 合作试验占比
    return [country, country_count, radio, co_count, co_radio]


def get_country_top(paper_number_excel, trail_number_excel, all_number_excel, paper_result_excel, trail_result_excel,
                    all_result_excel, paper_top10_excel, trail_top10_excel):
    """
    获取前10表格
    1. 论文top10--发文量，占比，平均被引频次，h-index, 合作论文数目, 合作论文数目本国占比
    2. 试验top10
    3. 一起top10
    4. 一起top10的论文
    5. 一起top10的试验
    :param paper_number_excel: paper 发文量文件
    :param trail_number_excel: trail 发文量文件
    :param all_number_excel: 一起 发文量文件
    :param paper_result_excel: paper top10表格
    :param trail_result_excel: trail top10表格
    :param all_result_excel: 一起 top10表格
    :param paper_top10_excel: 一起top10 paper表格
    :param trail_top10_excel: 一起top10 trail表格
    :return:
    """
    # 国家-top10分析（论文，试验，一起）
    # 论文分析--确定前10发文量不同，发文量，占比，平均被引频次，h-index, 合作论文数目, 合作论文数目本国占比
    conn, cursor = get_connection()
    # ----论文分析(要单独考虑欧洲)----
    # # 获取并检查数据
    data_paper = pd.read_excel(paper_number_excel)
    paper_count = list(data_paper['number'])
    if paper_count[11] == paper_count[12]:
        print('paper发文量排名11的国家和排名10的国家发文量相同，请人工确定如何进行分析！！！')
    # 获得结果
    sum_sql = 'select count(paper_id) from paper'
    cursor.execute(sum_sql)
    sum_count = cursor.fetchone()[0]
    paper_result = []
    for index, row in data_paper.head(12).iterrows():
        result_country = get_some_country_paper_info(row['country'], row['number'], sum_count, cursor)
        paper_result.append(result_country)
    columns = ['国家', '发文量', '发文量占比', '平均被引频次', 'h_index', '合作论文数量', '合作论文数目占本国发文量比值']
    paper_result = pd.DataFrame(paper_result, columns=columns)
    paper_result.to_excel(paper_result_excel, index=None)

    # ----试验分析----
    # 获取并检查数据
    data_trail = pd.read_excel(trail_number_excel)
    trail_count = list(data_trail['number'])
    if trail_count[11] == trail_count[12]:
        print('trail发文量排名11的国家和排名10的国家发文量相同，请人工确定如何进行分析！！！')
    # 获得结果
    sum_sql = 'select count(id) from trail'
    cursor.execute(sum_sql)
    sum_count = cursor.fetchone()[0]
    trail_result = []
    for index, row in data_trail.head(12).iterrows():
        result_country = get_some_country_trail_info(row['country'], row['number'], sum_count, cursor)
        trail_result.append(result_country)
    columns = ['国家', '试验量', '试验量占比', '合作试验数量', '合作试验数目占本国发文量比值']
    trail_result = pd.DataFrame(trail_result, columns=columns)
    trail_result.to_excel(trail_result_excel, index=None)

    # ----合在一起----
    # 获取并检查数据
    data_all = pd.read_excel(all_number_excel)
    all_count = list(data_all['number'])
    if all_count[11] == all_count[12]:
        print('paper和trail发文量排名11的国家和排名10的国家发文量相同，请人工确定如何进行分析！！！')
    # 获得结果
    sum_sql = 'select sum(nu) from (select count(id) as nu from trail union select count(paper_id) as nu from paper) a'
    cursor.execute(sum_sql)
    sum_count = cursor.fetchone()[0]
    all_result = []
    for index, row in data_all.head(12).iterrows():
        result_country = get_some_country_all_info(row['country'], row['number'], sum_count, cursor)
        all_result.append(result_country)
    columns = ['国家', '成果量', '成果量占比', '合作成果数量', '合作成果数目占本国成果量比值']
    all_result = pd.DataFrame(all_result, columns=columns)
    all_result.to_excel(all_result_excel, index=None)

    top_list = list(data_all.head(10)['country'])
    paper_top10 = data_paper[data_paper['country'].isin(top_list)]
    # ----合在一起top10论文----
    # 获得结果
    sum_sql = 'select count(paper_id) from paper'
    cursor.execute(sum_sql)
    sum_count = cursor.fetchone()[0]
    paper_result = []
    for index, row in paper_top10.iterrows():
        result_country = get_some_country_paper_info(row['country'], row['number'], sum_count, cursor)
        paper_result.append(result_country)
    columns = ['国家', '发文量', '发文量占比', '平均被引频次', 'h_index', '合作论文数量', '合作论文数目占本国发文量比值']
    paper_result = pd.DataFrame(paper_result, columns=columns)
    paper_result.to_excel(paper_top10_excel, index=None)
    # ----合在一起top10试验----
    trail_top10 = data_trail[data_trail['country'].isin(top_list)]
    # 获得结果
    sum_sql = 'select count(id) from trail'
    cursor.execute(sum_sql)
    sum_count = cursor.fetchone()[0]
    trail_result = []
    for index, row in trail_top10.head(10).iterrows():
        result_country = get_some_country_trail_info(row['country'], row['number'], sum_count, cursor)
        trail_result.append(result_country)
    columns = ['国家', '试验量', '试验量占比', '合作试验数量', '合作试验数目占本国发文量比值']
    trail_result = pd.DataFrame(trail_result, columns=columns)
    trail_result.to_excel(trail_top10_excel, index=None)
    close_connection(conn, cursor)


def country_top10_together(paper_number_excel, trail_number_excel, all_number_excel, to_file):
    data_paper = pd.read_excel(paper_number_excel).head(12).tail(10)
    data_paper['type'] = '论文'
    data_trail = pd.read_excel(trail_number_excel).head(12).tail(10)
    data_trail['type'] = '试验'
    data_all = pd.read_excel(all_number_excel).head(12).tail(10)
    data_all['type'] = '一起'
    result = data_paper.append(data_trail)
    result = result.append(data_all)
    result.to_excel(to_file, index=None)


def get_country_paper_month(country, cursor):
    """
    获取某国家各个月份论文量
    :param country:
    :param cursor:
    :return:
    """
    sql = """
        select a.publish_month, IFNULL(b.num,0) as num	from 
          (select distinct `number` as `publish_month` FROM `number` where `number` <= 12 and `number` >=1 ) a
        left join 
            (select `month`+0 as `publish_month`, count(*) as num  from paper where paper_id in 
                ( SELECT paper_id  FROM paper_country where `country_clear` = '%s') group by `month` 
            ) b
        on a.`publish_month`= b.`publish_month` 
        order by a.publish_month asc
    """ % country
    if country == 'europe':
        sql = """
                select a.publish_month, IFNULL(b.num,0) as num	from 
                  (select distinct `number` as `publish_month` FROM `number` where `number` <= 12 and `number` >=1 ) a
                left join 
                    (select `month`+0 as `publish_month`, count(*) as num  from paper where paper_id in 
                        ( SELECT paper_id  FROM paper_country where is_eu = 1) group by `month` 
                    ) b
                on a.`publish_month`= b.`publish_month` 
                order by a.publish_month asc
            """
    if country == 'non-europe':
        sql = """
                select a.publish_month, IFNULL(b.num,0) as num	from 
                  (select distinct `number` as `publish_month` FROM `number` where `number` <= 12 and `number` >=1 ) a
                left join 
                    (select `month`+0 as `publish_month`, count(*) as num  from paper where paper_id in 
                        ( SELECT paper_id  FROM paper_country where is_eu = 0) group by `month` 
                    ) b
                on a.`publish_month`= b.`publish_month` 
                order by a.publish_month asc
            """
    cursor.execute(sql)
    result = cursor.fetchall()
    result_all = pd.DataFrame(result, columns=['month', 'number'])
    return list(result_all['number'])


def get_country_trial_month(country, cursor):
    """
    获取某国家各个月份试验量
    :param country:
    :param cursor:
    :return:
    """
    sql = """
        select a.publish_month, IFNULL(b.num,0) as num	from 
          (select distinct `number` as `publish_month` FROM `number` where `number` <= 12 and `number` >=1 ) a
        left join 
            (select `month`+0 as `publish_month`, count(*) as num  from trail where id in 
                ( SELECT paper_id  FROM trial_country where `country` = '%s') group by `month` 
            ) b
        on a.`publish_month`= b.`publish_month` 
        order by a.publish_month asc
    """ % country
    if country == 'europe':
        sql = """
                select a.publish_month, IFNULL(b.num,0) as num	from 
                  (select distinct `number` as `publish_month` FROM `number` where `number` <= 12 and `number` >=1 ) a
                left join 
                    (select `month`+0 as `publish_month`, count(*) as num  from trail where id in 
                        ( SELECT paper_id  FROM trial_country where is_eu = 1) group by `month` 
                    ) b
                on a.`publish_month`= b.`publish_month` 
                order by a.publish_month asc
            """
    if country == 'non-europe':
        sql = """
                select a.publish_month, IFNULL(b.num,0) as num	from 
                  (select distinct `number` as `publish_month` FROM `number` where `number` <= 12 and `number` >=1 ) a
                left join 
                    (select `month`+0 as `publish_month`, count(*) as num  from trail where id in 
                        ( SELECT paper_id  FROM trial_country where is_eu = 0) group by `month` 
                    ) b
                on a.`publish_month`= b.`publish_month` 
                order by a.publish_month asc
            """
    cursor.execute(sql)
    result = cursor.fetchall()
    result_all = pd.DataFrame(result, columns=['month', 'number'])
    return list(result_all['number'])


def country_top10_month(paper_number_excel, trail_number_excel, all_number_excel, paper_result_excel,
                        trial_result_excel, all_result_excel, paper_top10_excel, trial_top10_excel):
    """
    # 国家每月发文量（论文，试验，总的,用总的前10的国家论文，试验）
    # 国家列表
    # 查询paper 并 返回 月份， 按照月份统计
    :param paper_number_excel:
    :param trail_number_excel:
    :param all_number_excel:
    :param paper_result_excel:
    :param trial_result_excel:
    :param all_result_excel:
    :param paper_top10_excel:
    :param trial_top10_excel:
    :return:
    """
    conn, cursor = get_connection()
    paper_top10_list = list(pd.read_excel(paper_number_excel).head(12).tail(10)['country'])
    trail_top10_list = list(pd.read_excel(trail_number_excel).head(12).tail(10)['country'])
    all_top10_list = list(pd.read_excel(all_number_excel).head(12).tail(10)['country'])
    # 列名称
    columns = list(range(1, 13))
    columns = [str(i) for i in columns]
    columns = ['国家'] + columns
    # ---论文---
    paper_result = []
    for country in paper_top10_list:
        result_country = get_country_paper_month(country, cursor)
        paper_result.append([country] + result_country)
    paper_result = pd.DataFrame(paper_result, columns=columns)
    paper_result.to_excel(paper_result_excel, index=None)
    # ---试验---
    trial_result = []
    for country in trail_top10_list:
        result_country = get_country_trial_month(country, cursor)
        trial_result.append([country] + result_country)
    trial_result = pd.DataFrame(trial_result, columns=columns)
    trial_result.to_excel(trial_result_excel, index=None)
    # ---论文和试验top10 一起---
    all_result = []
    for country in all_top10_list:
        result_country1 = get_country_paper_month(country, cursor)
        result_country2 = get_country_trial_month(country, cursor)
        result_country = [result_country1[i] + result_country2[i] for i in list(range(len(result_country1)))]
        result_country = [country] + result_country
        all_result.append(result_country)
    trial_result = pd.DataFrame(all_result, columns=columns)
    trial_result.to_excel(all_result_excel, index=None)
    # ---论文和试验top10 论文---
    paper_result = []
    for country in all_top10_list:
        result_country = get_country_paper_month(country, cursor)
        paper_result.append([country] + result_country)
    paper_result = pd.DataFrame(paper_result, columns=columns)
    paper_result.to_excel(paper_top10_excel, index=None)
    # ---论文和试验top10 试验---
    trial_result = []
    for country in all_top10_list:
        result_country = get_country_trial_month(country, cursor)
        trial_result.append([country] + result_country)
    trial_result = pd.DataFrame(trial_result, columns=columns)
    trial_result.to_excel(trial_top10_excel, index=None)
    close_connection(conn, cursor)


# ----------------------------------介入手段更新后数据处理方式----------------------------------
def get_intervention_number(to_file, label):
    """
    获得介入手段的结果（放在一个文件里）
    :param to_file:
    :param label: 介入手段是 ‘topic’ , 层次聚类是label
    :return:
    """
    conn, cursor = get_connection()
    # ---论文---
    paper_sql = """
    select TRIM(top_ipc) as `keyword plus`, count(*) as `number` from 
(SELECT substring_index(substring_index(sub_ipc,',',`help_topic_id`+1),',',-1) as `top_ipc` 
FROM mysql.`help_topic` , (select topic as sub_ipc 
from `paper` ) as a 
where  
   mysql.help_topic.help_topic_id < (LENGTH(sub_ipc)-LENGTH(REPLACE(sub_ipc,',',''))+1) ) as b
 where b.top_ipc is not NULL and b.top_ipc != ''
 GROUP BY TRIM(top_ipc)
 order by TRIM(top_ipc) desc
    """
    cursor.execute(paper_sql)
    paper_result = cursor.fetchall()
    paper_result = pd.DataFrame(paper_result, columns=['label', 'paper'])
    # ---试验---
    trail_sql = """
    select TRIM(top_ipc) as `keyword plus`, count(*) as `number` from 
    (SELECT substring_index(substring_index(sub_ipc,',',`help_topic_id`+1),',',-1) as `top_ipc` 
    FROM mysql.`help_topic` , (select topic as sub_ipc 
    from `trail` ) as a 
    where  
       mysql.help_topic.help_topic_id < (LENGTH(sub_ipc)-LENGTH(REPLACE(sub_ipc,',',''))+1) ) as b
     where b.top_ipc is not NULL and b.top_ipc != ''
     GROUP BY TRIM(top_ipc)
     order by TRIM(top_ipc) desc
    """
    cursor.execute(trail_sql)
    trail_result = cursor.fetchall()
    trail_result = pd.DataFrame(trail_result, columns=['label', 'trial'])
    # 一起和结果
    result = pd.merge(paper_result, trail_result, on='label')
    result['together'] = result.apply(lambda x: x['paper'] + x['trial'], axis=1)
    result.to_excel(to_file, index=None)
    close_connection(conn, cursor)


def get_intervention_month(paper_result_excel, trial_result_excel, all_result_excel, label, label_file):
    """
    获取 论文，试验，一起 的 介入手段 或者 类别时序（1-12个月）
    :param paper_result_excel:
    :param trial_result_excel:
    :param all_result_excel:
    :param label: 类别还是介入手段
    :param label_file: label的文件，get_type_number方法的结果文件
    :return:
    """
    # 修改月份映射
    month_json = {'1': 'Jan.', '2': 'Feb.', '3': 'Mar.', '4': 'Apr.', '5': 'May', '6': 'June', '7': 'July', '8': 'Aug.',
                  '9': 'Sept.', '10': 'Oct.', '11': 'Nov.', '12': 'Dec.'}
    conn, cursor = get_connection()
    # 列表
    label_list = list(pd.read_excel(label_file)['label'])
    # 列名称
    columns = list(range(1, 13))
    columns = [str(i) for i in columns]
    columns = ['label'] + columns
    # 查询语句
    sql = """           
        select a.publish_month, IFNULL(b.num,0) as num	from
                  (select distinct `number` as `publish_month` FROM `number` where `number` <= 12 and `number` >=1 ) a
                left join
                    (select `month`+0 as `publish_month`, count(*) as num  from %s where FIND_IN_SET('%s',topic)  group by `month` ) b
                on a.`publish_month`= b.`publish_month`
                order by a.publish_month asc
            """
    # ---论文---
    paper_result = []
    for label_one in label_list:
        paper_sql = sql % ('paper', label_one)
        cursor.execute(paper_sql)
        result = cursor.fetchall()
        result = pd.DataFrame(result, columns=['month', label_one])
        paper_result.append([label_one] + list(result[label_one]))
    paper_result = pd.DataFrame(paper_result, columns=columns, index=label_list)
    paper_result.columns = [month_json[i] if month_json.__contains__(i) else i for i in list(paper_result.columns)]
    paper_result.to_excel(paper_result_excel, index=None)
    # ---试验---
    trail_result = []
    for label_one in label_list:
        trail_sql = sql % ('trail', label_one)
        cursor.execute(trail_sql)
        result = cursor.fetchall()
        result = pd.DataFrame(result, columns=['month', label_one])
        trail_result.append([label_one] + list(result[label_one]))
    trail_result = pd.DataFrame(trail_result, columns=columns, index=label_list)
    trail_result.columns = [month_json[i] if month_json.__contains__(i) else i for i in list(trail_result.columns)]
    trail_result.to_excel(trial_result_excel, index=None)
    # 一起的结果，把上面两个相加
    all_result = []
    for label_one in label_list:
        paper_one = list(paper_result.loc[label_one])
        trail_one = list(trail_result.loc[label_one])
        result = [paper_one[i] + trail_one[i] for i in list(range(1, len(paper_one)))]
        all_result.append([label_one] + result)
    all_result = pd.DataFrame(all_result, columns=columns, index=label_list)
    all_result.columns = [month_json[i] if month_json.__contains__(i) else i for i in list(all_result.columns)]
    all_result.to_excel(all_result_excel, index=None)
    close_connection(conn, cursor)


def get_country_paper_intervention(country, label, cursor):
    """
    获取某国家各个类别论文量
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
                        ( SELECT paper_id  FROM paper_country where `country_clear` = '%s') group by `publish_month` 
                ) bb
        on FIND_IN_SET(aa.`publish_month`,bb.`publish_month` )
        ) c 
        group by c.publish_month
        order by c.publish_month
    """ % country
    if country == 'europe':
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
                        ( SELECT paper_id  FROM paper_country where is_eu = 1) group by `publish_month` 
                ) bb
        on FIND_IN_SET(aa.`publish_month`,bb.`publish_month` )
        order by aa.publish_month  
        ) c 
        group by c.publish_month
        order by c.publish_month
        """
    if country == 'non-europe':
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
                        ( SELECT paper_id  FROM paper_country where is_eu = 0) group by `publish_month` 
                ) bb
        on FIND_IN_SET(aa.`publish_month`,bb.`publish_month` )
        order by aa.publish_month 
        ) c 
        group by c.publish_month
        order by c.publish_month
	"""
    cursor.execute(sql)
    result = cursor.fetchall()
    result_all = pd.DataFrame(result, columns=['label', 'number'])
    return list(result_all['number'])


def get_country_trial_intervention(country, label, cursor):
    """
    获取某国家各个类别试验量
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
                    from `trail` ) as a 
                    where  
                         mysql.help_topic.help_topic_id < (LENGTH(sub_ipc)-LENGTH(REPLACE(sub_ipc,',',''))+1) ) as b
                     where b.top_ipc is not NULL and b.top_ipc != ''
                     GROUP BY TRIM(top_ipc)
                     order by TRIM(top_ipc) desc 
                ) aa
            left join 
                    (select topic as `publish_month`, count(*) as num  from trail where id in 
                            ( SELECT paper_id  FROM trial_country where country = '%s') group by `publish_month` 
                    ) bb
            on FIND_IN_SET(aa.`publish_month`, bb.`publish_month` )
            order by aa.publish_month
            ) c 
        group by c.publish_month
        order by c.publish_month
    """ % country
    if country == 'europe':
        sql = """
            select c.publish_month, IFNULL(SUM(num),0) as num	from (
            select aa.publish_month, IFNULL(bb.num,0) as num	from 
            (select TRIM(top_ipc) as `publish_month`, count(*) as `number` from 
                (SELECT substring_index(substring_index(sub_ipc,',',`help_topic_id`+1),',',-1) as `top_ipc` 
                FROM mysql.`help_topic` , (select topic as sub_ipc 
                from `trail` ) as a 
                where  
                     mysql.help_topic.help_topic_id < (LENGTH(sub_ipc)-LENGTH(REPLACE(sub_ipc,',',''))+1) ) as b
                 where b.top_ipc is not NULL and b.top_ipc != ''
                 GROUP BY TRIM(top_ipc)
                 order by TRIM(top_ipc) desc 
            ) aa
            left join 
                    (select topic as `publish_month`, count(*) as num  from trail where id in 
                            ( SELECT paper_id  FROM trial_country where is_eu = 1) group by `publish_month` 
                    ) bb
            on FIND_IN_SET(aa.`publish_month`, bb.`publish_month` )
            order by aa.publish_month 
            ) c 
            group by c.publish_month
            order by c.publish_month
            """
    if country == 'non-europe':
        sql = """
                select c.publish_month, IFNULL(SUM(num),0) as num	from (
                select aa.publish_month, IFNULL(bb.num,0) as num	from 
                (select TRIM(top_ipc) as `publish_month`, count(*) as `number` from 
                    (SELECT substring_index(substring_index(sub_ipc,',',`help_topic_id`+1),',',-1) as `top_ipc` 
                    FROM mysql.`help_topic` , (select topic as sub_ipc 
                    from `trail` ) as a 
                    where  
                         mysql.help_topic.help_topic_id < (LENGTH(sub_ipc)-LENGTH(REPLACE(sub_ipc,',',''))+1) ) as b
                     where b.top_ipc is not NULL and b.top_ipc != ''
                     GROUP BY TRIM(top_ipc)
                     order by TRIM(top_ipc) desc 
                ) aa
            left join 
                    (select topic as `publish_month`, count(*) as num  from trail where id in 
                            ( SELECT paper_id  FROM trial_country where is_eu = 0) group by `publish_month` 
                    ) bb
            on FIND_IN_SET(aa.`publish_month`, bb.`publish_month` )
            order by aa.publish_month
            ) c 
				group by c.publish_month
				order by c.publish_month
            """
    cursor.execute(sql)
    result = cursor.fetchall()
    result_all = pd.DataFrame(result, columns=['label', 'number'])
    return list(result_all['number'])


def country_top10_intervention(paper_number_excel, trail_number_excel, all_number_excel, paper_result_excel,
                       trial_result_excel, all_result_excel, paper_top10_excel, trial_top10_excel, label):
    """
    # 国家每个类别的发文量（论文，试验，总的,用总的前10的国家论文，试验）
    # 国家列表
    # 查询paper 并 返回 月份， 按照月份统计
    :param label: 标签
    :param paper_number_excel: 用来获取前10国家
    :param trail_number_excel: 用来获取前10国家
    :param all_number_excel: 用来获取前10国家
    :param paper_result_excel:
    :param trial_result_excel:
    :param all_result_excel:
    :param paper_top10_excel:
    :param trial_top10_excel:
    :return:
    """
    conn, cursor = get_connection()
    paper_top10_list = list(pd.read_excel(paper_number_excel).head(12).tail(10)['country'])
    trail_top10_list = list(pd.read_excel(trail_number_excel).head(12).tail(10)['country'])
    all_top10_list = list(pd.read_excel(all_number_excel).head(12).tail(10)['country'])
    # 列名称
    sql = """
    select TRIM(top_ipc) as `keyword plus` from 
    (SELECT substring_index(substring_index(sub_ipc,',',`help_topic_id`+1),',',-1) as `top_ipc` 
    FROM mysql.`help_topic` , (select topic as sub_ipc 
    from `trail` ) as a 
    where  
       mysql.help_topic.help_topic_id < (LENGTH(sub_ipc)-LENGTH(REPLACE(sub_ipc,',',''))+1) ) as b
     where b.top_ipc is not NULL and b.top_ipc != ''
     GROUP BY TRIM(top_ipc)
     order by TRIM(top_ipc) 
    """
    cursor.execute(sql)
    columns = cursor.fetchall()
    columns = pd.DataFrame(columns, columns=['label'])
    columns = ['国家'] + list(columns['label'])
    # 论文
    paper_result = []
    for country in paper_top10_list:
        result_country = get_country_paper_intervention(country, label, cursor)
        paper_result.append([country] + result_country)
    paper_result = pd.DataFrame(paper_result, columns=columns)
    paper_result.to_excel(paper_result_excel, index=None)
    # ---试验---
    trial_result = []
    for country in trail_top10_list:
        result_country = get_country_trial_intervention(country, label, cursor)
        trial_result.append([country] + result_country)
    trial_result = pd.DataFrame(trial_result, columns=columns)
    trial_result.to_excel(trial_result_excel, index=None)
    # ---论文和试验top10 一起---
    all_result = []
    for country in all_top10_list:
        result_country1 = get_country_paper_intervention(country, label, cursor)
        result_country2 = get_country_trial_intervention(country, label, cursor)
        result_country = [result_country1[i] + result_country2[i] for i in list(range(len(result_country1)))]
        result_country = [country] + result_country
        all_result.append(result_country)
    trial_result = pd.DataFrame(all_result, columns=columns)
    trial_result.to_excel(all_result_excel, index=None)
    # ---论文和试验top10 论文---
    paper_result = []
    for country in all_top10_list:
        result_country = get_country_paper_intervention(country, label, cursor)
        paper_result.append([country] + result_country)
    paper_result = pd.DataFrame(paper_result, columns=columns)
    paper_result.to_excel(paper_top10_excel, index=None)
    # ---论文和试验top10 试验---
    trial_result = []
    for country in all_top10_list:
        result_country = get_country_trial_intervention(country, label, cursor)
        trial_result.append([country] + result_country)
    trial_result = pd.DataFrame(trial_result, columns=columns)
    trial_result.to_excel(trial_top10_excel, index=None)
    close_connection(conn, cursor)


# ----------------------------------介入手段和分类部分（几乎相同，所以合并了）----------------------------------
def get_type_number(to_file, label):
    """
    获得介入手段的结果（放在一个文件里）
    :param to_file:
    :param label: 介入手段是 ‘topic’ , 层次聚类是label
    :return:
    """
    conn, cursor = get_connection()
    # ---论文---
    paper_sql = "select %s, count(*) from paper group by %s order by %s " % (label, label, label)
    cursor.execute(paper_sql)
    paper_result = cursor.fetchall()
    paper_result = pd.DataFrame(paper_result, columns=['label', 'paper'])
    # ---试验---
    trail_sql = "select %s, count(*) from trail group by %s order by %s " % (label, label, label)
    cursor.execute(trail_sql)
    trail_result = cursor.fetchall()
    trail_result = pd.DataFrame(trail_result, columns=['label', 'trial'])
    # 一起和结果
    result = pd.merge(paper_result, trail_result, on='label')
    result['together'] = result.apply(lambda x: x['paper'] + x['trial'], axis=1)
    result.to_excel(to_file, index=None)
    close_connection(conn, cursor)


def get_type_month(paper_result_excel, trial_result_excel, all_result_excel, label, label_file):
    """
    获取 论文，试验，一起 的 介入手段 或者 类别时序（1-12个月）
    :param paper_result_excel:
    :param trial_result_excel:
    :param all_result_excel:
    :param label: 类别还是介入手段
    :param label_file: label的文件，get_type_number方法的结果文件
    :return:
    """
    month_json = {'1': 'Jan.', '2': 'Feb.', '3': 'Mar.', '4': 'Apr.', '5': 'May', '6': 'June', '7': 'July', '8': 'Aug.',
                  '9': 'Sept.', '10': 'Oct.', '11': 'Nov.', '12': 'Dec.'}
    conn, cursor = get_connection()
    # 列表
    label_list = list(pd.read_excel(label_file)['label'])
    # 列名称
    columns = list(range(1, 13))
    columns = [str(i) for i in columns]
    columns = ['label'] + columns
    # 查询语句
    sql = """
                select a.publish_month, IFNULL(b.num,0) as num	from
                  (select distinct `number` as `publish_month` FROM `number` where `number` <= 12 and `number` >=1 ) a
                left join
                    (select `month`+0 as `publish_month`, count(*) as num  from %s where %s = '%s' group by `month` ) b
                on a.`publish_month`= b.`publish_month`
                order by a.publish_month asc
            """
    # ---论文---
    paper_result = []
    for label_one in label_list:
        paper_sql = sql % ('paper', label, label_one)
        cursor.execute(paper_sql)
        result = cursor.fetchall()
        result = pd.DataFrame(result, columns=['month', label_one])
        paper_result.append([label_one] + list(result[label_one]))
    paper_result = pd.DataFrame(paper_result, columns=columns, index=label_list)
    paper_result.columns = [month_json[i] if month_json.__contains__(i) else i for i in list(paper_result.columns)]
    paper_result.to_excel(paper_result_excel, index=None)
    # ---试验---
    trail_result = []
    for label_one in label_list:
        trail_sql = sql % ('trail', label, label_one)
        cursor.execute(trail_sql)
        result = cursor.fetchall()
        result = pd.DataFrame(result, columns=['month', label_one])
        trail_result.append([label_one] + list(result[label_one]))
    trail_result = pd.DataFrame(trail_result, columns=columns, index=label_list)
    trail_result.columns = [month_json[i] if month_json.__contains__(i) else i for i in list(trail_result.columns)]
    trail_result.to_excel(trial_result_excel, index=None)
    # 一起的结果，把上面两个相加
    all_result = []
    for label_one in label_list:
        paper_one = list(paper_result.loc[label_one])
        trail_one = list(trail_result.loc[label_one])
        result = [paper_one[i] + trail_one[i] for i in list(range(1, len(paper_one)))]
        all_result.append([label_one] + result)
    all_result = pd.DataFrame(all_result, columns=columns, index=label_list)
    all_result.columns = [month_json[i] if month_json.__contains__(i) else i for i in list(all_result.columns)]
    all_result.to_excel(all_result_excel, index=None)
    close_connection(conn, cursor)


def get_country_paper_type(country, label, cursor):
    """
    获取某国家各个类别论文量
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
                        ( SELECT paper_id  FROM paper_country where `country_clear` = '%s') group by `publish_month` 
                ) b
        on a.`publish_month`= b.`publish_month` 
        order by a.publish_month 
    """ % (label, label, country)
    if country == 'europe':
        sql = """
            select a.publish_month, IFNULL(b.num,0) as num	from 
                (select distinct %s as `publish_month` FROM `paper` ) a
            left join 
                    (select %s as `publish_month`, count(*) as num  from paper where paper_id in 
                            ( SELECT paper_id  FROM paper_country where is_eu = 1) group by `publish_month` 
                    ) b
            on a.`publish_month`= b.`publish_month` 
            order by a.publish_month 
            """ % (label, label)
    if country == 'non-europe':
        sql = """
            select a.publish_month, IFNULL(b.num,0) as num	from 
                (select distinct %s as `publish_month` FROM `paper` ) a
            left join 
                    (select %s as `publish_month`, count(*) as num  from paper where paper_id in 
                            ( SELECT paper_id  FROM paper_country where is_eu = 0) group by `publish_month` 
                    ) b
            on a.`publish_month`= b.`publish_month` 
            order by a.publish_month 
            """ % (label, label)
    cursor.execute(sql)
    result = cursor.fetchall()
    result_all = pd.DataFrame(result, columns=['label', 'number'])
    return list(result_all['number'])


def get_country_trial_type(country, label, cursor):
    """
    获取某国家各个类别试验量
    :param label:
    :param country:
    :param cursor:
    :return:
    """
    sql = """
        select a.publish_month, IFNULL(b.num,0) as num	from 
            (select distinct %s as `publish_month` FROM `paper` ) a
        left join 
            (select %s as `publish_month`, count(*) as num  from trail where id in 
                    ( SELECT paper_id  FROM trial_country where `country` = '%s') group by `publish_month` 
            ) b
        on a.`publish_month`= b.`publish_month` 
        order by a.publish_month 
    """ % (label, label, country)
    if country == 'europe':
        sql = """
                select a.publish_month, IFNULL(b.num,0) as num	from 
                    (select distinct %s as `publish_month` FROM `paper` ) a
                left join 
                    (select %s as `publish_month`, count(*) as num  from trail where id in 
                            ( SELECT paper_id  FROM trial_country where is_eu = 1) group by `publish_month` 
                    ) b
                on a.`publish_month`= b.`publish_month` 
                order by a.publish_month 
            """ % (label, label)
    if country == 'non-europe':
        sql = """
                select a.publish_month, IFNULL(b.num,0) as num	from 
                    (select distinct %s as `publish_month` FROM `paper` ) a
                left join 
                    (select %s as `publish_month`, count(*) as num  from trail where id in 
                            ( SELECT paper_id  FROM trial_country where is_eu = 0) group by `publish_month` 
                    ) b
                on a.`publish_month`= b.`publish_month` 
                order by a.publish_month 
            """ % (label, label)
    cursor.execute(sql)
    result = cursor.fetchall()
    result_all = pd.DataFrame(result, columns=['label', 'number'])
    return list(result_all['number'])


def country_top10_type(paper_number_excel, trail_number_excel, all_number_excel, paper_result_excel,
                       trial_result_excel, all_result_excel, paper_top10_excel, trial_top10_excel, label):
    """
    # 国家每个类别的发文量（论文，试验，总的,用总的前10的国家论文，试验）
    # 国家列表
    # 查询paper 并 返回 月份， 按照月份统计
    :param label: 标签
    :param paper_number_excel: 用来获取前10国家
    :param trail_number_excel: 用来获取前10国家
    :param all_number_excel: 用来获取前10国家
    :param paper_result_excel:
    :param trial_result_excel:
    :param all_result_excel:
    :param paper_top10_excel:
    :param trial_top10_excel:
    :return:
    """
    conn, cursor = get_connection()
    paper_top10_list = list(pd.read_excel(paper_number_excel).head(12).tail(10)['country'])
    trail_top10_list = list(pd.read_excel(trail_number_excel).head(12).tail(10)['country'])
    all_top10_list = list(pd.read_excel(all_number_excel).head(12).tail(10)['country'])
    # 列名称
    sql = 'select distinct %s as `publish_month` FROM `paper` order by %s ' % (label, label)
    cursor.execute(sql)
    columns = cursor.fetchall()
    columns = pd.DataFrame(columns, columns=['label'])
    columns = ['国家'] + list(columns['label'])
    # 论文
    paper_result = []
    for country in paper_top10_list:
        result_country = get_country_paper_type(country, label, cursor)
        paper_result.append([country] + result_country)
    paper_result = pd.DataFrame(paper_result, columns=columns)
    paper_result.to_excel(paper_result_excel, index=None)
    # ---试验---
    trial_result = []
    for country in trail_top10_list:
        result_country = get_country_trial_type(country, label, cursor)
        trial_result.append([country] + result_country)
    trial_result = pd.DataFrame(trial_result, columns=columns)
    trial_result.to_excel(trial_result_excel, index=None)
    # ---论文和试验top10 一起---
    all_result = []
    for country in all_top10_list:
        result_country1 = get_country_paper_type(country, label, cursor)
        result_country2 = get_country_trial_type(country, label, cursor)
        result_country = [result_country1[i] + result_country2[i] for i in list(range(len(result_country1)))]
        result_country = [country] + result_country
        all_result.append(result_country)
    trial_result = pd.DataFrame(all_result, columns=columns)
    trial_result.to_excel(all_result_excel, index=None)
    # ---论文和试验top10 论文---
    paper_result = []
    for country in all_top10_list:
        result_country = get_country_paper_type(country, label, cursor)
        paper_result.append([country] + result_country)
    paper_result = pd.DataFrame(paper_result, columns=columns)
    paper_result.to_excel(paper_top10_excel, index=None)
    # ---论文和试验top10 试验---
    trial_result = []
    for country in all_top10_list:
        result_country = get_country_trial_type(country, label, cursor)
        trial_result.append([country] + result_country)
    trial_result = pd.DataFrame(trial_result, columns=columns)
    trial_result.to_excel(trial_top10_excel, index=None)
    close_connection(conn, cursor)


def get_paper_drugs(row):
    # 获取论文的药物
    result = []
    if row['topic'] == '药物':
        if row['type2_AB'].find('|') != -1:
            result.extend(eval(row['type2_AB'].split('|')[1].strip()))
        if row['type2_AB'].find('|') != -1:
            result.extend(eval(row['type2_AB'].split('|')[1].strip()))
        if row['type2_AB'].find('|') != -1:
            result.extend(eval(row['type2_AB'].split('|')[1].strip()))
    return str(list(set(result)))


def get_trail_drugs(x):
    # 获取论文的药物
    result = eval(x)
    if len(result) != 0:
        result = eval(result[0])
    return str(list(set(result)))


def get_drugs_number(paper_number_excel, trail_number_excel, paper_result_excel, trial_result_excel,
                     all_result_excel):
    """
    论文和试验的分类里的药物里，进行药物分析
    :param paper_number_excel: 论文文件
    :param trail_number_excel: 试验文件
    :param paper_result_excel: 论文结果文件
    :param trial_result_excel: 试验结果文件
    :param all_result_excel: 一起结果文件
    :return:
    """
    # 论文
    paper_data = pd.read_excel(paper_number_excel)
    paper_data['drugs'] = paper_data.apply(lambda x: get_paper_drugs(x), axis=1)
    result_paper = {}
    for drugs_data in list(paper_data['drugs']):
        for drug in eval(drugs_data):
            if result_paper.__contains__(drug):
                result_paper[drug] = result_paper[drug] + 1
            else:
                result_paper[drug] = 1
    result_all = result_paper
    result_paper = pd.DataFrame.from_dict(result_paper, orient='index', columns=['number'])
    result_paper['drug'] = list(result_paper.index)
    result_paper.sort_values(by=['number'], inplace=True, ascending=False)
    result_paper = result_paper[result_paper['drug'] != 'drug:']
    result_paper.to_excel(paper_result_excel, index=None)
    # 试验
    trail_data = pd.read_excel(trail_number_excel)
    trail_data['drugs'] = trail_data['drugs'].apply(lambda x: get_trail_drugs(x))
    result_trail = {}
    for drugs_data in list(trail_data['drugs']):
        for drug in eval(drugs_data):
            if result_trail.__contains__(drug):
                result_trail[drug] = result_trail[drug] + 1
            else:
                result_trail[drug] = 1
    # 总的
    for key, value in result_trail.items():
        if result_all.__contains__(key):
            result_all[key] = result_all[key] + value
        else:
            result_all[key] = value
    result_all = pd.DataFrame.from_dict(result_all, orient='index', columns=['number'])
    result_all['drug'] = result_all.index
    result_all = result_all[result_all['drug'] != 'drug:']
    result_all.sort_values(by=['number'], inplace=True, ascending=False)
    result_all.to_excel(all_result_excel, index=None)
    # 试验保存
    result_trail = pd.DataFrame.from_dict(result_trail, orient='index', columns=['number'])
    result_trail['drug'] = result_trail.index
    result_trail = result_trail[result_trail['drug'] != 'drug:']
    result_trail.sort_values(by=['number'], inplace=True, ascending=False)
    result_trail.to_excel(trial_result_excel, index=None)


def get_drugs_month_number(paper_number_excel, trail_number_excel, paper_result_excel, trial_result_excel,
                           all_result_excel):
    """
    论文和试验的分类里的药物里，进行药物分析
    :param paper_number_excel: 论文文件
    :param trail_number_excel: 试验文件
    :param paper_result_excel: 论文结果文件
    :param trial_result_excel: 试验结果文件
    :param all_result_excel: 一起结果文件
    :return:
    """
    columns = list(range(1, 13))
    # 论文--
    paper_data = pd.read_excel(paper_number_excel)
    paper_data['drugs'] = paper_data.apply(lambda x: get_paper_drugs(x), axis=1)
    result_paper_df = pd.DataFrame(columns=['month', 'drug', 'number'])
    trail_data = pd.read_excel(trail_number_excel)
    trail_data['drugs'] = trail_data['drugs'].apply(lambda x: get_trail_drugs(x))
    trail_data['month'] = trail_data['Date registration3'].apply(lambda x: int(str(x)[4:6]))
    result_trail_df = pd.DataFrame(columns=['month', 'drug', 'number'])
    result_all_df = pd.DataFrame(columns=['month', 'drug', 'number'])
    for month_one in columns:
        paper_data_sub = paper_data[paper_data['month'] == month_one]
        result_paper = {}
        for drugs_data in list(paper_data_sub['drugs']):
            for drug in eval(drugs_data):
                if result_paper.__contains__(drug):
                    result_paper[drug] = result_paper[drug] + 1
                else:
                    result_paper[drug] = 1
        result_all = result_paper
        result_paper = pd.DataFrame.from_dict(result_paper, orient='index', columns=['number'])
        result_paper['drug'] = list(result_paper.index)
        result_paper.sort_values(by=['number'], inplace=True, ascending=False)
        result_paper = result_paper[result_paper['drug'] != 'drug:']
        result_paper = result_paper.head(10)
        result_paper['month'] = month_one
        result_paper_df = pd.concat([result_paper_df, result_paper])
        # 试验
        trail_data_sub = trail_data[trail_data['month'] == month_one]
        result_trail = {}
        for drugs_data in list(trail_data_sub['drugs']):
            for drug in eval(drugs_data):
                if result_trail.__contains__(drug):
                    result_trail[drug] = result_trail[drug] + 1
                else:
                    result_trail[drug] = 1
        # 总的
        for key, value in result_trail.items():
            if result_all.__contains__(key):
                result_all[key] = result_all[key] + value
            else:
                result_all[key] = value
        result_all = pd.DataFrame.from_dict(result_all, orient='index', columns=['number'])
        result_all['drug'] = result_all.index
        result_all = result_all[result_all['drug'] != 'drug:']
        result_all.sort_values(by=['number'], inplace=True, ascending=False)
        result_all = result_all.head(10)
        result_all['month'] = month_one
        result_all_df = pd.concat([result_all_df, result_all])
        # 试验保存
        result_trail = pd.DataFrame.from_dict(result_trail, orient='index', columns=['number'])
        result_trail['drug'] = result_trail.index
        result_trail = result_trail[result_trail['drug'] != 'drug:']
        result_trail.sort_values(by=['number'], inplace=True, ascending=False)
        result_trail = result_trail.head(10)
        result_trail['month'] = month_one
        result_trail_df = pd.concat([result_trail_df, result_trail])
    result_paper_df.to_excel(paper_result_excel, index=None)
    result_trail_df.to_excel(trial_result_excel, index=None)
    result_all_df.to_excel(all_result_excel, index=None)


def get_drugs_country_number(country_file, paper_number_excel, trail_number_excel, paper_result_excel,
                             trial_result_excel, all_result_excel):
    """
    论文和试验的分类里的药物里，进行药物分析
    :param country_file:
    :param paper_number_excel: 论文文件
    :param trail_number_excel: 试验文件
    :param paper_result_excel: 论文结果文件
    :param trial_result_excel: 试验结果文件
    :param all_result_excel: 一起结果文件
    :return:
    """
    columns = list(pd.read_excel(country_file).head(10)['country'])
    conn, cursor = get_connection()
    sql_paper = """select distinct UT from paper
        where paper_id in (select paper_id from paper_country where country_clear = '%s') 
    """
    sql_eu = """select distinct UT from paper
        where paper_id in (select paper_id from paper_country where is_eu = 1) 
    """
    sql_non_eu = """select distinct UT from paper
            where paper_id in (select paper_id from paper_country where is_eu = 0) 
        """
    # 论文--
    paper_data = pd.read_excel(paper_number_excel)
    paper_data['drugs'] = paper_data.apply(lambda x: get_paper_drugs(x), axis=1)
    result_paper_df = pd.DataFrame(columns=['country', 'drug', 'number'])
    trail_data = pd.read_excel(trail_number_excel)
    trail_data['drugs'] = trail_data['drugs'].apply(lambda x: get_trail_drugs(x))
    trail_data['region'] = trail_data['region'].fillna('N/A')
    result_trail_df = pd.DataFrame(columns=['country', 'drug', 'number'])
    result_all_df = pd.DataFrame(columns=['country', 'drug', 'number'])
    for month_one in columns:
        if month_one == 'europe':
            cursor.execute(sql_eu)
        elif month_one == 'non-europe':
            cursor.execute(sql_non_eu)
        else:
            cursor.execute(sql_paper % month_one)
        ids = cursor.fetchall()
        ids = pd.DataFrame(ids, columns=['ids'])
        paper_data_sub = paper_data[paper_data['UT'].isin(list(ids['ids']))]
        result_paper = {}
        for drugs_data in list(paper_data_sub['drugs']):
            for drug in eval(drugs_data):
                if result_paper.__contains__(drug):
                    result_paper[drug] = result_paper[drug] + 1
                else:
                    result_paper[drug] = 1
        result_all = result_paper
        result_paper = pd.DataFrame.from_dict(result_paper, orient='index', columns=['number'])
        result_paper['drug'] = list(result_paper.index)
        result_paper.sort_values(by=['number'], inplace=True, ascending=False)
        result_paper = result_paper[result_paper['drug'] != 'drug:']
        result_paper = result_paper.head(10)
        result_paper['country'] = month_one
        result_paper_df = pd.concat([result_paper_df, result_paper])
        # 试验
        paper_trail_sub = trail_data[trail_data['region'].str.contains(month_one)]
        result_trail = {}
        for drugs_data in list(paper_trail_sub['drugs']):
            for drug in eval(drugs_data):
                if result_trail.__contains__(drug):
                    result_trail[drug] = result_trail[drug] + 1
                else:
                    result_trail[drug] = 1
        # 总的
        for key, value in result_trail.items():
            if result_all.__contains__(key):
                result_all[key] = result_all[key] + value
            else:
                result_all[key] = value
        result_all = pd.DataFrame.from_dict(result_all, orient='index', columns=['number'])
        result_all['drug'] = result_all.index
        result_all = result_all[result_all['drug'] != 'drug:']
        result_all.sort_values(by=['number'], inplace=True, ascending=False)
        result_all = result_all.head(10)
        result_all['country'] = month_one
        result_all_df = pd.concat([result_all_df, result_all])
        # 试验保存
        result_trail = pd.DataFrame.from_dict(result_trail, orient='index', columns=['number'])
        result_trail['drug'] = result_trail.index
        result_trail = result_trail[result_trail['drug'] != 'drug:']
        result_trail.sort_values(by=['number'], inplace=True, ascending=False)
        result_trail = result_trail.head(10)
        result_trail['country'] = month_one
        result_trail_df = pd.concat([result_trail_df, result_trail])
    result_paper_df.to_excel(paper_result_excel, index=None)
    result_trail_df.to_excel(trial_result_excel, index=None)
    result_all_df.to_excel(all_result_excel, index=None)
    close_connection(conn, cursor)


# ----------------------------------合作网络----------------------------------
def get_matrix(sql, cursor, file_name, word_list=None):
    """
    根据sql 获得矩阵
    :param word_list: word_list是共现矩阵需要的词，如果是None, 默认是data['name']字段
    :param sql:
    :param cursor:
    :param file_name:
    :return:
    """
    cursor.execute(sql)
    rows = cursor.fetchall()
    data = pd.DataFrame(rows, columns=['detail_id', 'name'])

    if word_list is None:
        word_list = list(set(data['name'].values))
    detail_id_list = list(set(data['detail_id'].values))

    word_matrix = np.zeros((len(word_list), len(word_list)))
    for detail_id in detail_id_list:
        data_with_detail_id = data[data['detail_id'] == detail_id]['name'].values.tolist()
        for i in data_with_detail_id:
            for j in data_with_detail_id:
                if i in word_list and j in word_list:
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
        for j in range(i + 1, len(word_list)):
            ii = word_list.index(word_list[i])
            jj = word_list.index(word_list[j])
            if word_matrix[ii][jj] > 0 and word_matrix[ii][jj] >= triple_limit and ii != jj:
                results.append([word_list[i], word_list[j], abs(word_matrix[ii][jj])])
    results_df = pd.DataFrame(results, columns=['source', 'target', 'Weight'])
    results_df.to_excel(triple_file_name, index=None)


def get_country_co_network(df_paper_file_name, node_paper_file_name, triple_paper_file_name,
                           df_trail_file_name, node_trail_file_name, triple_trail_file_name,
                           df_all_file_name, node_all_file_name, triple_all_file_name, node_limit, triple_limit):
    """
    国家合作网络信息获取--论文，试验，一起
    :param df_paper_file_name:
    :param node_paper_file_name:
    :param triple_paper_file_name:
    :param df_trail_file_name:
    :param node_trail_file_name:
    :param triple_trail_file_name:
    :param df_all_file_name:
    :param node_all_file_name:
    :param triple_all_file_name:
    :param node_limit:
    :param triple_limit:
    :return:
    """
    conn, cursor = get_connection()
    # 论文
    paper_sql = """
                select paper_id, country_clear 
                from paper_country 
                group by paper_id, country_clear 
                order by paper_id
            """
    get_matrix(paper_sql, cursor, df_paper_file_name)
    get_node(df_paper_file_name, node_paper_file_name, node_limit)
    get_triple_number(df_paper_file_name, node_paper_file_name, triple_paper_file_name, triple_limit)
    # 试验
    trail_sql = """
    select paper_id, country 
    from trial_country 
    where country is not null 
    group by paper_id, country 
    order by paper_id
    """
    get_matrix(trail_sql, cursor, df_trail_file_name)
    get_node(df_trail_file_name, node_trail_file_name, node_limit)
    get_triple_number(df_trail_file_name, node_trail_file_name, triple_trail_file_name, triple_limit)
    # 一起
    all_sql = """
        select paper_id, country_clear as country 
        from paper_country 
        group by paper_id, country_clear 
        union ALL
        select  CONCAT(paper_id,'hhh') as paper_id, country 
        from trial_country 
        group by paper_id, country 
        """
    get_matrix(all_sql, cursor, df_all_file_name)
    get_node(df_all_file_name, node_all_file_name, node_limit)
    get_triple_number(df_all_file_name, node_all_file_name, triple_all_file_name, triple_limit)
    close_connection(conn, cursor)


def get_org_co_network(df_paper_file_name, node_paper_file_name, triple_paper_file_name, node_limit, triple_limit):
    """
    机构合作网络信息获取--论文
    :param df_paper_file_name:
    :param node_paper_file_name:
    :param triple_paper_file_name:
    :param node_limit:
    :param triple_limit:
    :return:
    """
    conn, cursor = get_connection()
    # 论文
    paper_sql = """
                select paper_id, CONCAT(org_clear,',',country_clear)
                from paper_country 
                group by paper_id, country_clear, org_clear 
                order by paper_id
            """
    word_list_sql = """
        SELECT CONCAT(org_clear,',',country_clear), count(DISTINCT paper_id) as num
        FROM paper_country
        GROUP BY country_clear, org_clear
        order by num desc
    """
    cursor.execute(word_list_sql)
    rows = cursor.fetchall()
    data = pd.DataFrame(rows, columns=['name', 'number'])
    data = data[data['number'] >= 10]
    word_list = list(data['name'])
    get_matrix(paper_sql, cursor, df_paper_file_name, word_list)
    get_node(df_paper_file_name, node_paper_file_name, node_limit)
    get_triple_number(df_paper_file_name, node_paper_file_name, triple_paper_file_name, triple_limit)

    close_connection(conn, cursor)


def get_author_co_network(df_paper_file_name, node_paper_file_name, triple_paper_file_name,
                          df_trail_file_name, node_trail_file_name, triple_trail_file_name,
                          df_all_file_name, node_all_file_name, triple_all_file_name, node_limit, triple_limit):
    """
    作者合作网络信息获取--论文，试验，一起
    :param df_paper_file_name:
    :param node_paper_file_name:
    :param triple_paper_file_name:
    :param df_trail_file_name:
    :param node_trail_file_name:
    :param triple_trail_file_name:
    :param df_all_file_name:
    :param node_all_file_name:
    :param triple_all_file_name:
    :param node_limit:
    :param triple_limit:
    :return:
    """
    conn, cursor = get_connection()
    # 论文
    paper_sql = """
                select paper_id, author 
                from paper_author 
                group by paper_id, author 
                order by paper_id
            """
    paper_word_list_sql = """
            SELECT author, count(DISTINCT paper_id) as num
            FROM paper_author
            GROUP BY author
            order by num desc
        """
    cursor.execute(paper_word_list_sql)
    rows = cursor.fetchall()
    data = pd.DataFrame(rows, columns=['name', 'number'])
    data = data[data['number'] >= 3]
    word_list = list(data['name'])
    get_matrix(paper_sql, cursor, df_paper_file_name, word_list)
    get_node(df_paper_file_name, node_paper_file_name, node_limit)
    get_triple_number(df_paper_file_name, node_paper_file_name, triple_paper_file_name, triple_limit)
    # 试验
    trail_sql = """
    select paper_id, author 
    from trail_author 
    group by paper_id, author 
    order by paper_id
    """
    trail_word_list_sql = """
            SELECT author, count(DISTINCT paper_id) as num
            FROM trail_author
            GROUP BY author
            order by num desc
            """
    cursor.execute(trail_word_list_sql)
    rows = cursor.fetchall()
    data = pd.DataFrame(rows, columns=['name', 'number'])
    data = data[data['number'] >= 2]
    word_list = list(data['name'])
    get_matrix(trail_sql, cursor, df_trail_file_name, word_list)
    get_node(df_trail_file_name, node_trail_file_name, node_limit)
    get_triple_number(df_trail_file_name, node_trail_file_name, triple_trail_file_name, triple_limit)
    # 一起
    all_sql = """
        select paper_id, author 
        from paper_author 
        group by paper_id, author 
        union ALL
        select CONCAT(paper_id,'hhh') as paper_id, author 
        from trail_author 
        group by paper_id, author 
        """
    all_word_list_sql = """
                select author, sum(num) from (
                SELECT author, count(DISTINCT paper_id) as num
                        FROM paper_author
                        GROUP BY author
                UNION ALL								
                SELECT author, count(DISTINCT paper_id) as num
                        FROM trail_author
                        GROUP BY author
                        ) a
                group by author
                order by sum(num) desc
                """
    cursor.execute(all_word_list_sql)
    rows = cursor.fetchall()
    data = pd.DataFrame(rows, columns=['name', 'number'])
    data = data[data['number'] >= 3]
    word_list = list(data['name'])
    get_matrix(all_sql, cursor, df_all_file_name, word_list)
    get_node(df_all_file_name, node_all_file_name, node_limit)
    get_triple_number(df_all_file_name, node_all_file_name, triple_all_file_name, triple_limit)
    close_connection(conn, cursor)


def get_txt_file(source_file, target_file, keep_columns):
    """
    转格式，中间用；隔开
    :param source_file:
    :param target_file:
    :param keep_columns: 是否保留标题
    :return:
    """
    data = pd.read_excel(source_file)
    f = open(target_file, 'w', encoding='utf-8')
    if keep_columns:
        f.write(';'.join(['id', 'label', 'weight']) + '\n')
    for index, row in data.iterrows():
        m = [str(i) for i in list(row)]
        f.write(';'.join(m) + '\n')
    f.close()


# ----------------------------------作者部分----------------------------------
def get_author_number(paper_number_excel, trail_number_excel, all_number_excel):
    """
    获取作者 试验，论文和总的的发文量
    :param paper_number_excel:
    :param trail_number_excel:
    :param all_number_excel:
    :return:
    """
    conn, cursor = get_connection()
    # ----试验，论文发文量----
    # 论文数目
    sql_paper = '''
        select author, count(*) as num from 
        paper_author 
        group by author, paper_id 
        order by num desc
    '''
    cursor.execute(sql_paper)
    result_paper = cursor.fetchall()
    result_paper = pd.DataFrame(result_paper, columns=['country', 'number'])
    # 试验数目
    sql_trail = '''
        select author, count(*) as num from 
        trail_author 
        group by author, paper_id 
        order by num desc
    '''
    cursor.execute(sql_trail)
    result_trail = cursor.fetchall()
    result_trail = pd.DataFrame(result_trail, columns=['country', 'number'])
    # 总数目
    sql_all = '''
            select author, num from (
            select author, count(*) as num from 
            paper_author 
            group by author, paper_id 
            union ALL 
            select author, count(*) as num from 
            trail_author 
            group by author, paper_id 
            )a  
            order by num desc
        '''
    cursor.execute(sql_all)
    result_all = cursor.fetchall()
    result_all = pd.DataFrame(result_all, columns=['country', 'number'])
    # 存储
    result_paper.to_excel(paper_number_excel, index=None)
    result_trail.to_excel(trail_number_excel, index=None)
    result_all.to_excel(all_number_excel, index=None)
    close_connection(conn, cursor)
