from flask import render_template, redirect, request, session
from waffle_app import app
from waffle_app.models.waffle_model import Waffle

@app.route('/dashboard')
def home():
    waffles = Waffle.get_all_with_users()

    return render_template('dashboard.html', waffles = waffles)


@app.route('/new/waffle')
def new():
    if not 'uuid' in session:
        return redirect('/')

    return render_template('new.html')


@app.route('/waffle/create', methods=['POST'])
def create_waffle():

    data = {
        **request.form,
        'user_id' : session['uuid']
    }

    if Waffle.validate(data):
        Waffle.create(data)

        return redirect('/dashboard')
        
    else:
        return redirect('/new/waffle')


@app.route('/images')
def show_images():

    waffles = Waffle.get_all_with_users()

    return render_template('images.html', waffles = waffles)


@app.route('/edit/waffle/<int:id>')
def edit(id):
    if not 'uuid' in session:
        return redirect('/dashboard')
    
    waffle = Waffle.get_one_with_users(id)

    return render_template('edit.html', waffle=waffle)


@app.route('/update/waffle', methods=['POST'])
def update_waffle():
    data = {
        **request.form,
        'user_id' : session['uuid']
    }

    if Waffle.validate(data):
        Waffle.update(data)
    else:
        return redirect(f'/edit/waffle/{request.form["id"]}')

    print(request.form)
    return redirect('/dashboard')


@app.route('/delete/waffle/<int:id>')
def delete(id):
    if not 'uuid' in session:
        return redirect('/dashboard')

    Waffle.delete(id)
    return redirect('/dashboard')
