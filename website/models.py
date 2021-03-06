from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.String(30))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Bookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(500))
    page_link = db.Column(db.String(500))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))






class Profiles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codechef = db.Column(db.String(200))
    codeforces = db.Column(db.String(200))
    atcoder = db.Column(db.String(200))
    hackerrank = db.Column(db.String(200))
    leetcode = db.Column(db.String(200))
    hackerearth = db.Column(db.String(200))
    github = db.Column(db.String(200))
    devfolio = db.Column(db.String(200))
    pwebsite = db.Column(db.String(200))
    linkedin = db.Column(db.String(200))
    city = db.Column(db.String(200))
    country = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    content = db.Column(db.String(10000))
    type= db.Column(db.String(200))
    date = db.Column(db.String(30))
    author=db.Column(db.String(150))
    img_link= db.Column(db.String(100))
    contactid=db.Column(db.String(100))
    rel_institution = db.Column(db.String(350)) 
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class competitions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    content = db.Column(db.String(10000))
    organization= db.Column(db.String(400))
    deadline= db.Column(db.String(80))
    fromdate = db.Column(db.String(80))
    todate = db.Column(db.String(80))
    open_to= db.Column(db.String(200))
    author=db.Column(db.String(150))
    reg_link= db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class internships_job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(200))
    type= db.Column(db.String(90))
    role = db.Column(db.String(300))
    stipend_sal= db.Column(db.String(400))
    role_desc= db.Column(db.String(800))
    deadline = db.Column(db.String(80))
    duration = db.Column(db.String(150))
    extra_benefits = db.Column(db.String(300))
    author=db.Column(db.String(150))
    reg_link= db.Column(db.String(200))
    open_to= db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(150))
    password = db.Column(db.String(150))
    full_name = db.Column(db.String(150))
    institution_name= db.Column(db.String(350))
    gender= db.Column(db.String(20))
    notes = db.relationship('Note')
    profiles = db.relationship('Profiles')
    posts = db.relationship('Posts')
    bookmarks = db.relationship('Bookmark')

