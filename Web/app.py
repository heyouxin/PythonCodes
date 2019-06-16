# -*- coding: utf-8 -*-
"""

-------------------------------------------------
   File Name：        app
   Description :
   Author :           heyouxin
   Create date：      2019/3/16
   Latest version:    v1.0.0
-------------------------------------------------
   Change Log:
#-----------------------------------------------#
    v1.0.0            hyx        2019/3/16
    1.
#-----------------------------------------------#
-------------------------------------------------

"""
import pandas as pd
from flask import Flask, jsonify, request, abort,url_for,render_template,redirect
from time import time
import json
from bson.objectid import ObjectId
from bson.json_util import dumps
import pymongo
from model import character_model

app = Flask(__name__)

mongo = pymongo.MongoClient('127.0.0.1', 27017)
db = mongo.brcweb

@app.route('/')
def index():
    return  render_template('index.html')

@app.route('/index/character',methods=['GET','POST'])
def character():
    if request.method == 'GET':
        print(000)
        questions = db.vocation_test.find({})
        questions = pd.DataFrame(list(questions))
        questions = questions.loc[:,['序号','问题','A','B','C']]
        questions = questions.rename(columns={'序号':'order_number','问题':'question'})
        questions_json = questions.to_json(force_ascii=False,orient='records')
        #questions_json = json.loads(questions_json)
        #return  render_template('index.html',questions_json=questions_json)
        return questions_json
    if request.method == 'POST':
        print("999")
@app.route('/index/character/submit', methods=['POST'])
def result():

    #answer_json = request.form.get('answer_json')
    data = request.get_data()
    j_data = json.loads(data)
    #anser_json = json.loads(j_data.values())
    print(j_data)
    #print(anser_json)
    #print(j_data.values()[0])
    for v in j_data.values():
        #print(k)
        answer_json = json.loads(v)
    print(answer_json)
    print(type(answer_json))

    answer_list = []
    #str = [{"a":1},{"b":2},None]
    for s in answer_json:
        if s==None:
            answer_list.append(None)
        else:
            #print(list(s.values())[0])
            if list(s.values())[1] == 1:
                answer_list.append('A')
            if list(s.values())[1] == 2:
                answer_list.append('B')
            if list(s.values())[1] == 3:
                answer_list.append('C')

    #str.values()
    #list(str[0].values())[0]
    #answer_json = filter(None, answer_json)
    #answer_list = [list(s.values())[0] for s in answer_json]
    print(answer_list)
    #print(answer_json.items())


    res = character_model(answer_list)
    #res = rule_score[['type','score']]
    res_json = res.to_json(force_ascii=False, orient='records')
    print(res_json)
    #res_json = json.loads(res_json)
    return res_json
    #return render_template('character_result.html', res_json=res_json)


'''
@app.route('/<content>/finished')
def finish(content):
    result = db.test.update_one(
        {'name':content},
        {
            '$set': {
                'is_finished': True,
                'finished_at': time()
            }
        }
    )
    return redirect('/')

@app.route('/<content>')
def delete(content):
    result = db.test.delete_one(
        {'name':content}
    )
    return redirect('/')
'''
if __name__ == '__main__':
    from werkzeug.contrib.fixers import ProxyFix
    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.run(debug=True,host='127.0.0.1', port=8080)
