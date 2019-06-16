# -*- coding: utf-8 -*-
"""

-------------------------------------------------
   File Name：        model
   Description :
   Author :           heyouxin
   Create date：      2019/3/29
   Latest version:    v1.0.0
-------------------------------------------------
   Change Log:
#-----------------------------------------------#
    v1.0.0            hyx        2019/3/29
    1.
#-----------------------------------------------#
-------------------------------------------------

"""
import pandas as pd
import pymongo
import json
from scipy.stats import norm
def preOperate():
    # 数据清洗
    question = pd.read_excel('data/question.xlsx')
    question = question.fillna('xxx')

    question_2 = question.loc[((question['序号'] == 'A') | (question['序号'] == 'B') | (question['序号'] == 'C')), :]
    question_3 = question_2.pivot(columns='序号', values='答案')
    question_3 = question_3.apply(lambda x: x.dropna().reset_index(drop=True))
    question_3 = question_3.reset_index(drop=True)

    question_4 = question.loc[~((question['序号'] == 'A') | (question['序号'] == 'B') | (question['序号'] == 'C')), :]
    question_4 = question_4.reset_index(drop=True)
    df = pd.concat([question_3, question_4], 1)

    df = df.rename(columns={'答案': '问题'})
    df2 = df.loc[:, ['序号', '问题', 'A', 'B', 'C']]
    df2.to_excel('data/questions.xlsx', index=False, encoding='utf8')

def insertDB():
    # 批量插入数据
    df2 = pd.read_excel('data/questions.xlsx')
    mongo = pymongo.MongoClient('127.0.0.1', 27017)
    db = mongo.vocation_test
    records = json.loads(df2.T.to_json()).values()
    db['question'].insert(records)

def seleDB():

    mongo = pymongo.MongoClient('127.0.0.1', 27017)
    db = mongo.brcweb
    questions = db.vocation_test.find({})
    questions = pd.DataFrame(list(questions))
    questions = questions.loc[:,['序号','问题','A','B','C']]
    questions = questions.rename(columns={'序号': 'order_number', '问题': 'question'})
    questions_json = questions.to_json(force_ascii=False,orient='records')

    fileObject = open('data/question.json', 'w', encoding="utf-8")
    fileObject.write(questions_json)
    fileObject.close()


def character_model(answer_list=None):
    type =[ [3 ,26,27,51,52,76,101,126,151,176],
              [28,53,54,77,78,102,103,127,128,152,153,177,178],
              [4,5,29,30,55,79,80,104,105,129,130,154,179],
              [6,7,31,32,56,57,81,106,131,155,156,180,181],
              [8,33,58,82,83,107,108,132,133,157,158,182,183],
              [9,34,59,84,109,134,159,160,184,185],
              [10,35,36,60,61,85,86,110,111,135,136,161,186],
              [11,12,37,62,87,112,137,138,162,163],
              [13,38,63,64,88,89,113,114,139,164],
              [14,15,39,40,65,90,91,115,116,140,141,165,166],
              [16,17,41,42,66,67,92,117,142,167],
              [18,19,43,44,68,69,93,94,118,119,143,144,168],
              [20,21,45,46,70,95,120,145,169,170],
              [22,47,71,72,96,97,121,122,146,171],
              [23,24,48,73,98,123,147,148,172,173],
              [25,49,50,74,75,99,100,124,125,149,150,174,175]]

    A = [0]*187
    B = [0]*187
    C = [0]*187
    d = {"A":A,"B":B,"C":C}
    df_score = pd.DataFrame(d)
    rule1 = {28:"B", 53:"B", 54:"B", 77:"C", 78:"B", 102:"C", 103:"B", 127:"C", 128:"B", 152:"B", 153:"C", 177:"A", 178:"A"}
    for (k,v) in rule1.items():
        k = k-1
        df_score.loc[k,v] = df_score.loc[k,v]+1

    rule2 = {3:"A", 4:"A", 5:"C", 6:"C", 7:"A", 8:"C", 9:"C", 10:"A", 11:"C", 12:"C", 13:"A",
    14:"C", 15:"C", 16:"C", 17:"A", 18:"A", 19:"C", 20:"A", 21:"A", 22:"C", 23:"C", 24:"C", 25:"A", 26:"C", 27:"C", 29:"C",
    30:"A", 31:"C", 32:"C", 33:"A", 34:"C", 35:"C", 36:"A", 37:"A", 38:"A", 39:"A", 40:"A", 41:"C", 42:"A", 43:"A", 44:"C",
    45:"C", 46:"A", 47:"A", 48:"A", 49:"A", 50:"A", 51:"C", 52:"A", 55:"A", 56:"A", 57:"C", 58:"A", 59:"A", 60:"C", 61:"C",
    62:"C", 63:"C", 64:"C", 65:"A", 66:"C", 67:"C", 68:"C", 69:"A", 70:"A", 71:"A", 72:"A", 73:"A", 74:"A", 75:"C", 76:"C",
    79:"C", 80:"C", 81:"C", 82:"C", 83:"C", 84:"C", 85:"C", 86:"C", 87:"C", 88:"A", 89:"C", 90:"C", 91:"A", 92:"C", 93:"C",
    94:"C", 95:"C", 96:"C", 97:"C", 98:"A", 99:"A", 100:"A", 101:"A", 104:"A", 105:"A", 106:"C", 107:"A",108:"A", 109:"A",
    110:"A", 111:"A", 112:"A", 113:"A", 114:"A", 115:"A", 116:"A", 117:"A", 118:"A", 119:"A", 120:"C", 121:"C",122:"C", 123:"C",
    124:"A", 125:"C", 126:"A", 129:"A", 130:"A", 131:"A", 132:"A", 133:"A", 134:"A", 135:"C", 136:"A", 137:"C", 138:"A", 139:"C",
    140:"A", 141:"C", 142:"A", 143:"A", 144:"C", 145:"A", 146:"A", 147:"A", 148:"A", 149:"A", 150:"A", 151:"C", 154:"C", 155:"A",
    156:"A", 157:"C", 158:"C", 159:"C", 160:"A", 161:"C", 162:"C", 163:"A", 164:"A", 165:"C", 166:"C", 167:"A", 168:"A", 169:"A",
    170:"C", 171:"A", 172:"C", 173:"A", 174:"A", 175:"C", 176:"A", 179:"A", 180:"A", 181:"A", 182:"A", 183:"A", 184:"A", 185:"A", 186:"A"}
    for (k,v) in rule2.items():
        k = k-1
        df_score.loc[k,v] = df_score.loc[k,v]+2
        df_score.loc[k, 'B'] = 1


    #test
    if answer_list==None:
        df_score['answer'] = 'A'
        df_score.loc[50:100,'answer']='B'
        df_score.loc[100:187,'answer']='C'
    else:
        df_score['answer'] = pd.Series(answer_list)
        df_score['answer'] = df_score['answer'].fillna('A')
    ###

    df_score['score'] = df_score.apply(set_score,axis=1)
    type_score = []
    for type_one in type:
        type_score.append(sum(df_score.loc[[t-1 for t in type_one],'score']))

    rule_score = pd.read_excel('data/raw_to_std.xlsx')
    rule_score = rule_score.applymap(lambda x : str(x))
    rule_score['raw_score'] = pd.Series(type_score).map(lambda x: int(x))
    rule_score['std_score'] = 0
    for r in range(0,len(rule_score)):
        for c in range(1,11):
            if rule_score.loc[r, 'raw_score'] in [int(s) for s in rule_score.iloc[r, c].split(',')]:
                rule_score.loc[r,'std_score'] = rule_score.columns[c]
    rule_score['平均分'] = rule_score['平均分'].map(lambda x: float(x))
    rule_score['标准差'] =  rule_score['标准差'].map(lambda x: float(x))
    rule_score['std_score'] =  rule_score['std_score'].map(lambda x: float(x))
    rule_score['percent'] = rule_score.apply(lambda x : norm.cdf(x['std_score'],x['平均分'],x['标准差']),axis=1)
    rule_score = rule_score.rename(columns={'因素':'type','percent':'score'})
    #rule_score[['type', 'score']]
    return rule_score[['type','score']]

def set_score(x):
    if x[3] == 'A':
        return x[0]
    if x[3] == 'B':
        return x[1]
    if x[3] == 'C':
        return x[2]


if __name__ == '__main__':
    pass



