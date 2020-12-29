from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class SettingForm(FlaskForm):
    color = StringField('Steel Color', validators=[DataRequired()])
    submit = SubmitField('save the setting')