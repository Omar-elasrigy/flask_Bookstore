from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField,IntegerField, SubmitField,FileField
from wtforms.validators import DataRequired, Length,Regexp
from app.models import Post, db
from flask_bootstrap import Bootstrap5


class PostForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(2, 40)
    ,Regexp(r'^[A-Za-z\s]+$', message="please type characters only")])
    description = StringField("Description",validators=[Length(5,50)])
    image= FileField("Image", validators=[DataRequired()])
    submit = SubmitField("add post")

class EditForm(FlaskForm):
    name = StringField("Name", validators=[ Length(2, 40)
    ,Regexp(r'^[A-Za-z\s]+$', message="please type characters only")])
    description = StringField("Description",validators=[Length(5,50)])
    image= FileField("Image")
    submit = SubmitField("edit post")