from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import InputRequired, Length, NumberRange

class UploadScoreForm(FlaskForm):
    class Meta:
        csrf = False
        locales = ['fr']
    username = StringField('username', validators=[
                        InputRequired(),
                        Length(min=2, max=63)])

    score = IntegerField('score', validators=[
        InputRequired(), NumberRange(min=0, max=9999999)])
