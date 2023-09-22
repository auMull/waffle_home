from flask import render_template, redirect, request, session
from waffle_app import app
from waffle_app.models.user_model import User


@app.route('/')
def index():
    return render_template('index.html')



@app.route('/create/user', methods=['POST'])
def new_user():


    if not User.validate(request.form):
        return redirect('/')

    User.register_user(request.form)
    return redirect('/')



@app.route('/signin/user', methods=['POST'])
def sign_in():

    login = User.login_user(request.form)
    session['uname'] = request.form['username']
    if login:
        session['uuid'] = login.id
        return redirect('/dashboard')

    return redirect('/')



@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')