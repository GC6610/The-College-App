from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Bookmark, Note,User,Profiles,Posts ,competitions, internships_job
from . import db
import json
from datetime import datetime, timedelta
import os
views = Blueprint('views', __name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))


###           Home Page        ###
@views.route('/dashboard', methods=['GET'])
@login_required
def home():
    quotes=["The gem cannot be polished without friction, nor man perfected without trials.",
           "Everyone who got where he is has had to begin where he was.",
           "Remember, you can earn more money, but when time is spent is gone forever.",
           "It's your aptitude, not just your attitude that determines your ultimate altitude.",
           "We will either find a way, or make one.",
           "To reach a great height a person needs to have great depth.",
           "No dream comes true until you wake up and go to work.",
           "Wind to thy wings. Light to thy path. Dreams to thy heart."]
    return render_template("menu.html", details=[current_user,quotes])
###           Home Page Ends       ###

###           TaskPage         ###

@views.route('/tasks', methods=['GET', 'POST'])
@login_required
def task():
    if request.method == 'POST':

        note = request.form.get('note')
        deadline=request.form.get('task-deadline')
        try:
            month=['January','February','March','April','May','June','July','August','September','October','November','December']
            deadline=deadline.split('T')
            task_date=deadline[0].split('-')
            task_year=task_date[0]
            task_month=month[int(task_date[1])-1]
            task_day=task_date[2]
            task_time=deadline[1]


            present = datetime.now()
            flg= present.year==int(task_year) and present.month==int(task_date[1]) and present.day==int(task_day)
            if  flg and (int(task_time[:2])<present.hour or (int(task_time[:2])==present.hour and int(task_time[3:5])<=present.minute)):
                flash('Time has already passed', category='error')

            elif (not flg) and datetime(int(task_year),int(task_date[1]),int(task_day)) < present:
                flash('Date has already passed', category='error')


            elif len(note) < 1:
                flash('Note is too short!', category='error')
            else:
                deadline = task_time + ' ' + task_day + ' ' + task_month + ' ' + task_year
                new_note = Note(data=note, date=deadline,user_id=current_user.id)
                db.session.add(new_note)
                db.session.commit()
                
                
        except:
            if len(note) < 1:
                flash('Note is too short!', category='error')
            else:

                new_note = Note(data=note, date="None",user_id=current_user.id)
                db.session.add(new_note)
                db.session.commit()
                note=""


    return render_template("tasks.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

###           TaskPage  Ends      ###

###           Profile Page        ###
@views.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method=='POST':
        name = request.form.get('name')

        city = request.form.get('city')
        country = request.form.get('country')
        p_website = request.form.get('personal')
        linkedin = request.form.get('linkedin')
        github = request.form.get('github')
        devfolio = request.form.get('devfolio')
        cc = request.form.get('codechef')
        cf = request.form.get('codeforces')
        ac = request.form.get('atcoder')
        hackerrank = request.form.get('hackerrank')
        leetcode = request.form.get('leetcode')
        hackerearth = request.form.get('hackerearth')


        user_n=User.query.get(current_user.id)
        user_n.full_name=name
        try:
            db.session.commit()
        except Exception as e:
            flash(e,category="error")
            db.session.rollback()
        user = Profiles.query.filter_by(user_id=current_user.id).first()
        if user:
            user.codechef=cc
            user.codeforces=cf
            user.atcoder=ac
            user.hackerrank=hackerrank
            user.leetcode=leetcode
            user.hackerearth=hackerearth
            user.github=github
            user.devfolio=devfolio
            user.pwebsite=p_website
            user.linkedin=linkedin
            user.city=city
            user.country=country
            try:
                db.session.commit()
            except Exception as e:
                flash(e, category="error")
                db.session.rollback()
        else:
            pf = Profiles(codechef=cc,codeforces=cf,atcoder=ac,hackerrank=hackerrank,leetcode=leetcode,
                          hackerearth=hackerearth,github=github,devfolio=devfolio,pwebsite=p_website,linkedin=linkedin,
                          city=city,country=country,user_id=current_user.id)
            db.session.add(pf)
            db.session.commit()


        print(current_user.profiles[0])
        return render_template("profile.html", user=current_user)

    user = Profiles.query.filter_by(user_id=current_user.id).first()
    if user:
        return render_template("profile.html",user=current_user)

    pf = Profiles(user_id=current_user.id)
    db.session.add(pf)
    db.session.commit()

    return render_template("profile.html", user=current_user)
###           Profile Page Ends       ###

###           Post        ###
@views.route('/inputpost', methods=['GET','POST'])
@login_required
def inputpost():
    if request.method=='POST':
        title = request.form.get('title')
        content = request.form.get('content')
        type=request.form.get('type')
       
        
        present=datetime.now()
        date=present.strftime("%d-%m-%Y")
        img_link=request.form.get('links')

           
        
        post = Posts(title=title,content=content,type=type,date=date,img_link=img_link,contactid=current_user.email,author=current_user.full_name,rel_institution=current_user.institution_name,user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        

        return render_template("postinput.html", user=current_user)
    return render_template("postinput.html", user=current_user)

@views.route('/buyorsell', methods=['GET'])
@login_required
def buyorsell():
   
    posts = Posts.query.filter_by(type="BuyorSell",rel_institution=current_user.institution_name).all()
    return render_template("posts.html", det=[current_user,posts])


@views.route('/lostandfound', methods=['GET'])
@login_required
def lostandfound():

    posts = Posts.query.filter_by(type="LostandFound",rel_institution=current_user.institution_name).all()
    return render_template("posts.html", det=[current_user,posts])


@views.route('/others', methods=['GET'])
@login_required
def otherposts():

    posts = Posts.query.filter_by(type="Others",rel_institution=current_user.institution_name).all()
    return render_template("posts.html", det=[current_user,posts])

@views.route('/myposts', methods=['GET'])
@login_required
def myposts():
   
    posts = Posts.query.filter_by(user_id=current_user.id).all()
    return render_template("myposts.html", det=[current_user,posts])

@views.route('/delete-post', methods=['POST'])
def delete_post():
    post = json.loads(request.data)
    postId = post['postId']
    post = Posts.query.get(postId)
    if post:
        if post.user_id == current_user.id:
            db.session.delete(post)
            db.session.commit()

    return jsonify({})


###           Post Ends        ###

###    bookmarks views and forms      ###

@views.route('/createbookmark', methods=['GET','POST'])
@login_required
def inputbookmark():
    if request.method=='POST':
        
        data = request.form.get('content')
        page_link=request.form.get('links')
        if data and page_link:
            bookmark = Bookmark(data=data,page_link=page_link,user_id=current_user.id)
            db.session.add(bookmark)
            db.session.commit()
        else:
            flash("Fill all the required credentials")
        

        
    return render_template("createbookmark.html", user=current_user)

@views.route('/bookmarks', methods=['GET'])
@login_required
def viewbookmark():
    return render_template("bookmark.html", user=current_user)


@views.route('/delete-bookmark', methods=['POST'])
def delete_bookmark():
    bookmark = json.loads(request.data)
    
    bookmarkId = bookmark['bookId']
    bookmark = Bookmark.query.get(bookmarkId)
    if bookmark:
        if bookmark.user_id == current_user.id:
            db.session.delete(bookmark)
            db.session.commit()

    return jsonify({})

###    bookmarks views and forms  Ends   ###


###    Internship/  views and forms      ###

@views.route('/internships', methods=['GET'])
@login_required
def internship():

    internships = internships_job.query.filter_by(type="INTERN").all()
    return render_template("job_internships.html", det=[current_user,internships])


@views.route('/jobs', methods=['GET'])
@login_required
def fulltime_offers():

    jobs = internships_job.query.filter_by(type="FULL TIME").all()
    return render_template("job_internships.html", det=[current_user,jobs])

@views.route('/jobinternform', methods=['GET', 'POST'])
@login_required
def jobinternform():
    if request.method == 'POST':

        company = request.form.get('org')
        type =request.form.get('type')
        role=request.form.get('role')
        stipend_sal=request.form.get('stipend')
        duration= request.form.get('duration')
        role_desc=request.form.get('desc')
        deadline=request.form.get('deadline')
        extra_benefits=request.form.get('extras')
        reg_link=request.form.get('link')
        open_to=request.form.get('author')
        
        try:
            month=['January','February','March','April','May','June','July','August','September','October','November','December']
            deadline=deadline.split('T')
            opp_date=deadline[0].split('-')
            opp_year=opp_date[0]
            opp_month=month[int(opp_date[1])-1]
            opp_day=opp_date[2]
            opp_time=deadline[1]

            
            deadline = opp_time + ' ' + opp_day + ' ' + opp_month + ' ' + opp_year
            new_opp = internships_job(company=company,type=type,role=role,stipend_sal=stipend_sal,duration=duration,role_desc=role_desc,deadline=deadline,extra_benefits=extra_benefits,author=current_user.full_name,reg_link=reg_link,open_to=open_to,user_id=current_user.id)
            db.session.add(new_opp)
            db.session.commit()
                
                
        except:
            flash("Error While Submission ",category="error")
            

               


    return render_template("job_internshipform.html", user=current_user)

@views.route('/delete-jobintern', methods=['POST'])
def delete_job():
    job = json.loads(request.data)
    
    jobId = job['jobId']
    job = internships_job.query.get(jobId)
    if job:
        if job.user_id == current_user.id:
            db.session.delete(job)
            db.session.commit()

    return jsonify({})
###    Internship & Jobs  views and forms  Ends    ###

###   Competition  views and forms      ###

@views.route('/competition', methods=['GET'])
@login_required
def competition():
    
    competitions_ =competitions.query.all()
    

    return render_template("competition.html", det=[current_user,competitions_])


@views.route('/competitionform', methods=['GET', 'POST'])
@login_required
def competitionform():
    if request.method == 'POST':
        
        title = request.form.get('title')
        organization = request.form.get('org')
        content =request.form.get('content')
        deadline=request.form.get('deadline')
        fromdate=request.form.get('fromdate')
        todate=request.form.get('todate')
        open_to=request.form.get('open_to')
        reg_link=request.form.get('link')
        
        try:
            def daycal(deadline):
                month=['January','February','March','April','May','June','July','August','September','October','November','December']
                deadline=deadline.split('T')
                opp_date=deadline[0].split('-')
                opp_year=opp_date[0]
                opp_month=month[int(opp_date[1])-1]
                opp_day=opp_date[2]
                opp_time=deadline[1]

                
                return opp_time + ' ' + opp_day + ' ' + opp_month + ' ' + opp_year
            deadline=daycal(deadline)
            fromdate=daycal(fromdate)
            todate=daycal(todate)
            new_competition = competitions(organization=organization,title=title,content=content,deadline=deadline,fromdate=fromdate,todate=todate,author=current_user.full_name,reg_link=reg_link,open_to=open_to,user_id=current_user.id)
            db.session.add(new_competition)
            db.session.commit()
                
                
        except:
            flash("Error While Submission ",category="error")
            

               


    return render_template("competitionform.html", user=current_user)



@views.route('/delete-competition', methods=['POST'])
def delete_competition():
    competition = json.loads(request.data)
    
    competitionId = competition['compId']
    competition = competitions.query.get(competitionId)
    if competition:
        if competition.user_id == current_user.id:
            db.session.delete(competition)
            db.session.commit()

    return jsonify({})


###   competition  views and forms  Ends    ###