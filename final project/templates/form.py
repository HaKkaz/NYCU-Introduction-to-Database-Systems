from flask_wtf import FlaskForm
from wtforms import StringField


class MyForm(FlaskForm):
    Sexual = SelectField(u'性別', choices=[('男','Male'),('女','Female'),('不願透漏','No Answer')])
    Age = SelectField(u'年齡', choices=['10~15','15~20','20~30'])
    submit = SubmitField('Submit')