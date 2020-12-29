# -*- coding:utf-8 -*-
# @Time    : 2020/8/22 14:24
# @Author  : Heying Zhu

'''
Split clean_after.csv file generated from the analysis_txt.py
'''

import pandas as pd
import datetime

# load data
def load_data():
    path = "D:/data/clean_after.csv"
    data = pd.read_csv(path)
    return data


if __name__ == "__main__":
    # The root directory where the data is stored
    save_root = "D:/code/data/"

    data = load_data()
    data = data.drop_duplicates(['AB', 'TI'], keep="first")
    data = data.reset_index()

    paper_need_col = ["TI", "AB", "DE", "ID", "SO", "PT", "PY", "SC", "LA", "WC"]
    paper = pd.DataFrame()              # table 1：paper basic info
    paper_country_org = pd.DataFrame()  # table 2：paper-country-org table
    paper_financial = pd.DataFrame()    # table 3：paper-financial table

    print("Begin：", datetime.datetime.now().strftime('%Y.%m.%d-%H:%M:%S'))
    for index, row in data.iterrows():
        # Table 1：One line corresponds to the generation of one record
        one_paper = {"id": index}
        for item in paper_need_col:
            if item in row and not pd.isnull(row[item]):
                one_paper[item] = row[item]
            else:
                one_paper[item] = None
        paper = paper.append([one_paper], ignore_index=True)

        # Table 2：C1 field splitting countries and institutions
        if "C1" in row and not pd.isnull(row["C1"]):
            address_list = row["C1"].split("\n   ")
            if "AF" in row and not pd.isnull(row["AF"]):
                author_list = row['AF'].split("\n")
            for one_address in address_list:
                country = one_address.split(",")[-1].strip()  # 拆分国家字段
                if one_address.find("[") >= 0 and one_address.find("]") >= 0:
                    org_remain = one_address.split("]")[1].strip()[:-len(country)-2]
                    org = one_address.split("]")[1].strip().split(",")[0]
                    team = one_address.split("]")[0].strip()
                    team = team[team.find("[")+1:]
                    # 把已经出现的作者删掉
                    team_split = team.split(",")
                    for one_aut in team:
                        if one_aut in author_list:
                            author_list.remove(one_aut)

                else:
                    org_remain = one_address.strip()[:-len(country)-2]
                    org = one_address.strip().split(",")[0]
                    team = ", ".join(author_list)
                one_record = {"paper_id":index, "country": country[:-1], "org": org, "org_type": None, "team": team}
        #         paper_country_org = paper_country_org.append([one_record], ignore_index=True)

        # 表3：FU字段拆分
        if "FU" in row and not pd.isnull(row["FU"]):
            financial_list = row['FU'].split(";")
            for one_financial in financial_list:
                if one_financial.find("[") != -1:
                    financial_name = one_financial[:one_financial.find("[")].strip()
                    financial_code = one_financial[one_financial.find("[")+1:one_financial.find("]")].strip()
                else:
                    financial_name = one_financial.strip()
                    financial_code = None
                # print("\none_financial  = ", one_financial)
                # print("financial_name = ", financial_name)
                paper_financial = paper_financial.append([{"paper_id": index, "financial_name": financial_name,
                                                           "financial_code": financial_code, "type": None}], ignore_index=True)

        if index%100 == 0 and index!=0:
            print("It has been processed ", index, "data！", datetime.datetime.now().strftime('%Y.%m.%d-%H:%M:%S'))

    # save tables
    data.to_csv(save_root + "paper_original_drop.csv", index=False)  # keep all the fields
    paper.to_csv(save_root + "paper.csv")
    paper_country_org.to_csv(save_root + "paper_country.csv")
    paper_financial.to_csv(save_root + "paper_financial_new.csv")

    print("The end！")


