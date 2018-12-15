from flask import Flask,render_template,redirect,url_for,session
from flask_wtf import FlaskForm,RecaptchaField
from wtforms import StringField, PasswordField,BooleanField,validators,SelectField,TextAreaField,RadioField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug import secure_filename
from wtforms.fields.html5 import EmailField 
import os
import sys

class PostForm(FlaskForm):
    title = StringField('TITLE ',validators=[validators.InputRequired()])
    topic = SelectField('TOPIC ',choices=[('algo',"Algorithm"),('ds',"Data Structures"),('m',"Math"),('phy',"Physics")])
    time = SelectField('TIME ',choices=[('1d',"1 Day"),('2d',"2 Day"),('3d',"3 Day"),('4d',"4 Day")])
    question = TextAreaField('QUESTION ', render_kw={"rows": 13, "cols": 11},validators=[validators.InputRequired()])
    answer = StringField('ANSWER ',validators=[validators.InputRequired()])
    

class LeaveReply(FlaskForm):
    message=TextAreaField('message',validators=[validators.InputRequired(),validators.Length(min=7)])
    spoiler=BooleanField('Might Include Answer')
    upload=upload = FileField('Picture', validators=[
        FileAllowed(['jpg', 'png'], 'Images only!')
    ])
    repliedMessageId=0 ## DEFAULT OLARAK HIC KIMSEYE CEVAP VERİLMİYOR.
    
class editMessageForm(FlaskForm):
    message=TextAreaField('Message',validators=[validators.InputRequired()])

class answerForm(FlaskForm):
    answer=StringField('Answer :',validators=[validators.InputRequired()])
    amount=StringField('Amount to Bet :',validators=[validators.InputRequired()])
    radio=RadioField('Label', choices=[('clan','In Behalf of Clan'),('individual','In Behalf of Myself')])
    
class clanForm(FlaskForm):
    clanName = StringField('Clan Name :',validators=[validators.InputRequired()])