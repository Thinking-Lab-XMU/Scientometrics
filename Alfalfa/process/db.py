# -*- coding:utf-8 -*-
# @Time    : 2020/9/2 21:11
# @Author  : Heying Zhu

'''
Connection and query of MySQL database
'''

import pymysql

# connect
def connect_db():
    cnx = pymysql.connect(host="127.0.0.1",port=3306, user="******",password ="******",database = "******",charset="utf8")
    cursor = cnx.cursor()
    return cnx, cursor

# query
def select_muxu_data(cnx, cursor, select_sql):

    try:
        cursor.execute(select_sql)
        results = cursor.fetchall()
        return results
    except:
        print("Query failed！")




if __name__ == "__main__":
    cnx, cursor = connect_db()
    select_sql = "SELECT TI, AB FROM paper"
    select_muxu_data(cnx, cursor, select_sql)