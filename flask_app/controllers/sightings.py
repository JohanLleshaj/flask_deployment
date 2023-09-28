from flask import render_template, redirect, session, request, flash
from flask_app import app
from flask_app.models.sighting import Sighting
from flask_app.models.user import User

@app.route('/new/sighting')
def new_sighting():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "user_id": session['user_id']
    }
    return render_template('new_sighting.html', user= User.get_by_id(data))

@app.route('/create/sighting', methods=['POST'])
def create_sighting():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Sighting.validate_sighting(request.form):
        return redirect('/new/sighting')
    data = {
        "location": request.form["location"],
        "description": request.form["description"],
        "numberOf": int(request.form["numberOf"]),
        "date_made": request.form["date_made"],
        "user_id": session["user_id"],
        "user_fullname": session["full_name"],
    }
    Sighting.save(data)
    return redirect('/dashboard')


@app.route('/destroy/sighting/<int:id>')
def destroy_sighting(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Sighting.destroy(data)
    return redirect('/')


@app.route('/sighting/<int:id>')
def show_sighting(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "sighting_id": id
    }
    userData = {
        "user_id": session['user_id']
    }
    clickedSighting = Sighting.getUsersWhoIsSkeptic(data)
    print(clickedSighting)
    return render_template('show_sighting.html', sighting = clickedSighting, user=User.get_by_id(userData))



@app.route('/edit/sighting/<int:id>')
def edit_sighting(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "sighting_id": id
    }
    userData = {
        "user_id": session['user_id']
    }
    return render_template('edit_sighting.html', edit = Sighting.get_one(data), user=User.get_by_id(userData))


@app.route('/update/sighting/', methods=['POST'])
def update_sighting():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Sighting.validate_sighting(request.form):
        return redirect(request.referrer)
    
    data = {
        "location": request.form["location"],
        "description": request.form["description"],
        "numberOf": int(request.form["numberOf"]),
        "date_made": request.form["date_made"],
        "sighting_id": request.form["id"],
    }
    Sighting.update(data)
    return redirect('/dashboard')


@app.route('/sighting/<int:id>/skeptic', methods=['GET','PUT'])
def skeptic_sighting(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data={
        'sighting_id': id,
        'user_id': session['user_id']
    }
    Sighting.addSkeptic(data)
    updatedSighting = Sighting.getUsersWhoIsSkeptic(data)
    updatedData = {
        'sighting_id': id,
        'dontTrust': updatedSighting.dontTrust
    }
    Sighting.updateSkeptic(updatedData)
    return render_template('show_sighting.html', sighting=updatedSighting,  user=User.get_by_id(data))


@app.route('/sighting/<int:id>/nonskeptic', methods=['GET','PUT'])
def nonSkeptic_sighting(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data={
        'sighting_id': id,
        'user_id': session['user_id']
    }
    User.nonSkeptic(data)
    updatedSighting = Sighting.getUsersWhoIsSkeptic(data)
    updatedData = {
        'sighting_id': id,
        'dontTrust': updatedSighting.dontTrust
    }
    Sighting.updateSkeptic(updatedData)
    return render_template('show_sighting.html', sighting=updatedSighting,  user=User.get_by_id(data))

