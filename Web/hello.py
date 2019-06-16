from flask import Flask, session, redirect, url_for, escape, request
from flask import render_template
from flask_pymongo import PyMongo
app=Flask(__name__)
app.config['MONGO_DBNAME'] = 'patent'
app.config['MONGO_URI'] = 'mongodb://root:123456@localhost:27017/patent'
mongo = PyMongo(app)


@app.route('/hell/')
@app.route('/hell/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

@app.route('/index/')
def hello2():
    return render_template('character_result.html')


'''
@app.route('/')
def show_entries():
    #results = mongo.db.patent_info.find({"appli_num":"CN00100002.0"})
    #entries=[123,456]
    #return render_template('show_entries.html', entries=entries)
    return render_template('show_entries.html')
'''

@app.route('/')
def user(name=None):
    if name is None:
        user = mongo.db.patent_info.find({'appli_num': "CN00100002.0"})
        print(user)
        if user is not None:
            return render_template('user.html', users=[user])
        else:
            return 'No user found!'

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'a':
            error = 'Invalid username'
        elif request.form['password'] != 'b':
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
        '''
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        '''

    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))


if __name__ == '__main__':
    app.run()