"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""
import os
from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from app.forms import LoginForm, NewPost, Search, ProPicUpload, CEForm, RegisterForm, CreateGrp
from werkzeug.utils import secure_filename

# from app.models import UserProfile


###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    srchForm = Search()
    return render_template('home.html', srchForm=srchForm)


@app.route('/about/')
def about():
    """Render the website's about page."""
    srchForm = Search()
    return render_template('about.html', srchForm=srchForm)


@app.route("/login", methods=["GET", "POST"])
def login():
    srchForm = Search()
    form = LoginForm()
    if request.method == "POST":
        # change this to actually validate the entire form submission
        # and not just one field
        if form.username.data:
            # Get the username and password values from the form.

            # using your model, query database for a user based on the username
            # and password submitted. Remember you need to compare the password hash.
            # You will need to import the appropriate function to do so.
            # Then store the result of that query to a `user` variable so it can be
            # passed to the login_user() method below.

            # get user id, load into session
            login_user(user)

            # remember to flash a message to the user
            return redirect(url_for("home"))  # they should be redirected to a secure-page route instead
    return render_template("login.html", form=form, srchForm=srchForm)

@app.route('/register', methods=['POST', 'GET'])
def register():
    """Render the website's about page."""
    srchForm = Search()
    form = RegisterForm()
    return render_template('register.html', form = form, srchForm=srchForm)


# user_loader callback. This callback is used to reload the user object from
# the user ID stored in the session
@login_manager.user_loader
def load_user(id):
    return UserProfile.query.get(int(id))



@app.route('/dashboard', methods=['POST', 'GET'])
def dashboard():
    srchForm = Search()
    form = NewPost()
    
    if request.method == 'POST' and srchForm.validate_on_submit():
        term = srchForm.searchTerm.data 
        results()
           
    if request.method == 'POST' and form.validate_on_submit():
        # Get file data and save to your uploads folder
        if form.photo.data: #for both text and photo
            photo = form.photo.data 
            description = form.description.data

            filename = secure_filename(photo.filename)
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return jsonify(message = [{"message" : "File Upload Successful", "filename": filename, "description": description}])
        
        else: #only posts text
            description = form.description.data 
            return jsonify(message = [{"message" : "Post Successful", "description": description}])
           
    return render_template('dashboard.html', form=form, srchForm = srchForm)


@app.route('/friends/', methods=['POST', 'GET'])
def friends():
    """Render the website's friends page."""
    srchForm = Search()
    return render_template('friends.html', srchForm = srchForm)


@app.route('/results/', methods=['POST', 'GET'])
def results():
    srchForm = Search()
    return render_template('results.html', srchForm = srchForm)


@app.route('/profile/', methods=['POST', 'GET'])
def profile():
    """Render website's home page."""
    srchForm = Search()
    form = NewPost()
    uploadForm = ProPicUpload()

    if request.method == 'POST' and form.validate_on_submit():
        # Get file data and save to your uploads folder
        if form.photo.data: #for both text and photo
            photo = form.photo.data 
            description = form.description.data

            filename = secure_filename(photo.filename)
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return jsonify(message = [{"message" : "File Upload Successful", "filename": filename, "description": description}])
        
        else: #only posts text
            description = form.description.data 
            return jsonify(message = [{"message" : "Post Successful", "description": description}])

    if request.method == 'POST' and uploadForm.validate_on_submit(): 
        propic = uploadForm.propic.data 
        filename = secure_filename(propic.filename)
        propic.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    return render_template('profile.html', srchForm=srchForm, uploadForm = uploadForm, form = form)



@app.route('/yourgroups', methods=['POST', 'GET'])
def yourGroups():
    """Render Your Groups page"""
    srchForm = Search()
    form = CreateGrp()
    return render_template('your_groups.html', srchForm=srchForm, form = form)




@app.route('/grpProfile/', methods=['POST', 'GET'])
def grpProfile():
    """Render website's group profile page."""
    srchForm = Search()
    form = NewPost()
    uploadForm = ProPicUpload()
    ceForm = CEForm()

    if request.method == 'POST' and form.validate_on_submit():
        # Get file data and save to your uploads folder
        if form.photo.data: #for both text and photo
            photo = form.photo.data 
            description = form.description.data

            filename = secure_filename(photo.filename)
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return jsonify(message = [{"message" : "File Upload Successful", "filename": filename, "description": description}])
        
        else: #only posts text
            description = form.description.data 
            return jsonify(message = [{"message" : "Post Successful", "description": description}])

    if request.method == 'POST' and uploadForm.validate_on_submit(): 
        propic = uploadForm.propic.data 
        filename = secure_filename(propic.filename)
        propic.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    return render_template('group_profile.html', srchForm=srchForm, uploadForm=uploadForm, form=form, ceForm=ceForm)

###
# The functions below should be applicable to all Flask apps.
###

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    srchForm = Search()
    return render_template('404.html', srchForm=srchForm), 404


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8080")
