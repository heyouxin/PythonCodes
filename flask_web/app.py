# -*- coding: utf-8 -*-
"""

-------------------------------------------------
   File Name：        app
   Description :
   Author :           何友鑫
   Create date：      2019-03-18
   Latest version:    v1.0.0
-------------------------------------------------
   Change Log:
#-----------------------------------------------#
    v1.0.0            hyx        2019-03-18
    1.
#-----------------------------------------------#
-------------------------------------------------

"""

from flask import Flask, request, session, redirect, url_for, abort, \
    render_template, flash

from mysql_init import MySQL

app = Flask(__name__)
mysql = MySQL(app)

#获取数据库
def get_db():
    return mysql.connection.cursor()

#首页
@app.route('/show_entries')
def show_entries():

    cur = get_db()
    cur.execute('select code, SEC_NAME from bond_static order by id desc')
    entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    print(entries)
    return render_template('show_entries.html', entries=entries)


#登录页
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)


#添加条目
@app.route('/add_entry', methods=['POST'])
def add_entry():
    cur = get_db()
    if not session.get('logged_in'):
        abort(401)

    title = str(request.form['title'])
    text = str(request.form['text'])
    print()
    cur.execute('insert into entries (title, text) values (%s, %s)',
                [title,text])
    mysql.connection.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

#退出登录
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))


if __name__ == '__main__':
    app.run(debug=True)