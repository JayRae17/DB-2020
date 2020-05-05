from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import DataRequired, InputRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])


class NewPost(FlaskForm):
    description = TextAreaField('Description', validators=[InputRequired()])
    photo = FileField('Photo', validators=[FileAllowed(['jpg', 'png', 'Images only!'])])



class Search(FlaskForm):
    searchTerm = StringField('searchTerm', validators=[InputRequired()])


class ProPicUpload(FlaskForm):
    propic = FileField(validators=[FileRequired(),FileAllowed(['jpg', 'png', 'Images only!'])])