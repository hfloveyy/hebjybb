# -*- coding: utf-8 -*-

import sys
sys.path.insert(0,'f:/hebjybb')
sys.path.insert(0,'f:\hebjybb\env\lib\site-packages')


from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash

import sqlite3
from flask.ext.bootstrap import Bootstrap
import time





CONFIG_SETTINGS = 'config.py'

SECRET_KEY = 'development key'


app = Flask(__name__)

import db



app.config.from_pyfile('config.py')


app.secret_key = SECRET_KEY

bootstrap = Bootstrap(app)

jianqu_names = ['一监区','二监区','三监区','四监区','五监区','六监区','七监区',
'八监区','九监区','十监区','十一监区','十二监区','后勤监区','外籍监区','集训监区','出监监区','病犯监区','禁闭、严管','高戒备','改造业务科室']

def querylastdata(jianqu):
    sql = 'select * from jianqu where createtime = (select max(createtime) from jianqu where jianqu = \'%s\' )' % jianqu
    jianqu = db.query_db(sql)
    return jianqu

def querylastks():
    sql = 'select * from kanshou where createtime = (select max(createtime) from kanshou)'
    kanshou = db.query_db(sql)
    return kanshou

def total(content):
    total_list = []
    two = [0,0,0,0,0,0,0]
    one = []
    for some in content:
        one = []
        if len(some):
            three = some[0]
            for i in range(3,8):
                if three[i]:
                    one.append(int(str(three[i])))
                else:
                    one.append(0)
            #two = map(lambda (a,b):a+b, zip(one,two))
            two = [a+b for a, b in zip(one,two)]
    return two

def test_str(content):
    if content.isdigit():
        return content
    else:
        content = '0'
        return content

def queryall():
    sql = 'select * from kanshou'
    sql2 = 'select * from jianqu'
    kanshou = db.query_db(sql)
    jianqu = db.query_db(sql2)
    return kanshou,jianqu

def delete_all():
    sql = 'truncate table jianqu'
    if db.query_db(sql):
        return True
    else:
        return False


def get_time(timeStamp):
    timeArray = time.localtime(timeStamp)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return otherStyleTime













@app.route('/')
def index():
    content = []

    #查询最后一条信息
    for jianqu in jianqu_names:
        data = querylastdata(jianqu)
        content.append(data)
    number = list(content)

    kanshou = querylastks()

    total_list = total(content)
    #return render_template('index.html',number = number,kanshou = kanshou)
    return render_template('index.html',number = number,kanshou = kanshou,total = total_list) 
    

    


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if app.config[str(username)] != password:
            error = u'错误密码！'
        else:
            if username in 'JIANQU21':
                session['logged_in'] = False
                return render_template('addks.html', error=error)
            else:
                session['logged_in'] = True
                flash('You were logged in')
                return render_template('add.html', error=error)
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('index'))

@app.route('/add', methods=['GET', 'POST'])
def add():
    if 'logged_in' not in session:
        error = 'You need login!'
        return redirect(url_for('login'))
    if  not session['logged_in']:
        return redirect(url_for('addks'))
    if request.method == 'POST':
        jianqu = request.form['jianqu']
        zhibanlingdao = request.form['zhibanlingdao']
        baitianzaigang = test_str(request.form['baitianzaigang'])
        yejianzhiban = test_str(request.form['yejianzhiban'])
        zaice = test_str(request.form['zaice'])
        shiyou = test_str(request.form['shiyou'])
        chugong = test_str(request.form['chugong'])
        beizhu = request.form['beizhu']
        #create_time = time.time()
        create_time = get_time(time.time())

        conn = db.get_db()
        conn.execute('insert into jianqu (jianqu, zhibanlingdao,baitianzaigang,yejianzhiban,zaice,shiyou,chugong,beizhu,createtime) values (?, ?, ?, ?, ?, ?, ?, ?, ?)',\
            [jianqu,zhibanlingdao,baitianzaigang,yejianzhiban,zaice,shiyou,chugong,beizhu,create_time])
        conn.commit()
        flash('New entry was successfully posted')
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/addks', methods=['GET', 'POST'])
def addks():
    if 'logged_in' not in session:
        error = 'You need login!'
        return redirect(url_for('login'))
    if request.method == 'POST':
        zhibanlingdao = request.form['zhibanlingdao']
        damen = test_str(request.form['damen'])
        ermen = test_str(request.form['ermen'])
        sanmen = test_str(request.form['sanmen'])
        beizhu = request.form['beizhu']
        #create_time = time.time()
        create_time = get_time(time.time())

        conn = db.get_db()
        conn.execute('insert into kanshou (zhibanlingdao,damen,ermen,sanmen,beizhu,createtime) values (?, ?, ?, ?, ?, ?)',\
            [zhibanlingdao,damen,ermen,sanmen,beizhu,create_time])
        conn.commit()
        flash('New entry was successfully posted')
        return redirect(url_for('index'))
    return render_template('addks.html')


@app.route('/logging')
def logging():
    if 'logged_in' not in session:
        error = 'You need login!'
    kanshou,jianqu = queryall()
    return render_template('logging.html',kanshou = kanshou,jianqu = jianqu) 


    
'''
@app.route('/delete')
def delete():
    if 'logged_in' not in session:
        error = 'You need login!'
    if delete_all():
        print('delete all') '''




if __name__ == '__main__':
    app.secret_key = SECRET_KEY
    app.run(debug=True)
