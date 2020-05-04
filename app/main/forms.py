from flask_wtf import FlaskForm
from wtforms import SubmitField, PasswordField, StringField, SelectField,TextAreaField
from wtforms.validators import Required

class InForm(FlaskForm):
    pitch = TextAreaField('Tell it')
    title = StringField('Title')
    category = SelectField(u'info category', choices=[('visual', 'visual'), ('applied', 'applied'), ('perform', 'perform')])
    submit = SubmitField('Submit')

 
class lamentform(FlaskForm):
    comment = TextAreaField('lament')
    submit = SubmitField('Post lamentations')

class UpdateProfile(FlaskForm):
    bio = TextAreaField('About you', validators=[Required()])
    submit = SubmitField('submit')
    