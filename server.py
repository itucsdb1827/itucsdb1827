from flask import Flask,render_template,redirect,url_for,session
from flask_wtf import FlaskForm,RecaptchaField
from wtforms import StringField, PasswordField,BooleanField,validators
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug import secure_filename
from wtforms.fields.html5 import EmailField 
from topic import PostForm,LeaveReply,editMessageForm,answerForm,clanForm
import psycopg2
import datetime
from datetime import timedelta
from passlib.hash import pbkdf2_sha256 as hasher
import os
import sys

app = Flask(__name__)
adress="postgres://postgres:159753456@localhost:5432/postgres"
##adress="postgres://uyxegmizzcfgoj:3107cb2c0cfd9de6528ff9b966cd87d5040ec3dea13d85c863244efae597e6cb@ec2-54-225-241-25.compute-1.amazonaws.com:5432/d5uaci1fn1qp6d"

UPLOAD_FOLDER='static/avatars/'


    
    


app.config['SECRET_KEY']='ASD159sDGDAFHAFSghsrjrjeacaethehg21f65a1f65e153a1ae5v1a6e5v165gASD'
app.config['RECAPTCHA_PUBLIC_KEY']='6Ldz2nUUAAAAAAOxPyirz5W4T-o0IT-8Z1X9PMcZ'
app.config['RECAPTCHA_PRIVATE_KEY']='6Ldz2nUUAAAAAONNFYvLuTtrZOGNSKT90wHsiN0q'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

noUsernamePasswordFound='The username and password you entered did not match our records. Please double-check and try again.'


class SignUpForm(FlaskForm):##signupform
    username=StringField('Username:',validators=[validators.InputRequired(),validators.Length(min=6,max=16,message="Username must be between 6 and 16 characters.")])
    password1=PasswordField('Password:',validators=[validators.DataRequired(),validators.Length(min=6,max=16,message="Password must be between 6 and 16 characters."),validators.EqualTo('password2',message="passwords must be equal.")])
    password2=PasswordField('Password Again:',validators=[validators.DataRequired()])
    email1=EmailField('E-mail:',validators=[validators.InputRequired()])
    upload = FileField('Avatar', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png'], 'Images only!')
    ])
    checkbox=BooleanField('I read terms and conditions.',validators=[validators.InputRequired()])
    recaptcha=RecaptchaField()
    
class LoginForm(FlaskForm):##login form
    username=StringField('Username:',validators=[validators.InputRequired()])
    password=PasswordField('Password:',validators=[validators.DataRequired()])
    

class UserNameEditForm(FlaskForm): ##username edit 
    username=StringField('Username:',validators=[validators.InputRequired(),validators.Length(min=6,max=16,message="Username must be between 6 and 16 characters.")])

class PasswordEditForm(FlaskForm):## password edit
    password3=PasswordField('Old Password:',validators=[validators.DataRequired()])
    password1=PasswordField('New Password:',validators=[validators.DataRequired(),validators.Length(min=6,max=16,message="Password must be between 6 and 16 characters."),validators.EqualTo('password2',message="passwords must be equal.")])
    password2=PasswordField('New Password Again:',validators=[validators.DataRequired()])

class EmailEditForm(FlaskForm): ## email edit
    email1=EmailField('E-mail:',validators=[validators.InputRequired()])

class AvatarEditForm(FlaskForm): ##avatar edit
    upload = FileField('Avatar', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png'], 'Images only!')
    ])
def idToUserName(id): ## user id to username
    with psycopg2.connect(adress) as conn:
        cursor=conn.cursor()
        statement="""SELECT *FROM users WHERE id=%s"""
        cursor.execute(statement,(id,))
        line=cursor.fetchone()
        return str(line[1])
        
def UserNameToId(username):  ## username to user id
    with psycopg2.connect(adress) as conn:
        cursor=conn.cursor()
        statement="""SELECT *FROM users WHERE username=%s"""
        cursor.execute(statement,(username,))
        line=cursor.fetchone()
        return str(line[0]) 

def typeDefiner(List): ##check algorithm data structures math or physics
     with psycopg2.connect(adress) as conn:
        cursor=conn.cursor()
        statement="""SELECT topic FROM problems WHERE id=%s"""
        cursor.execute(statement,(List[5],))
        line=cursor.fetchone()
        return line[0]

def clanidtoname(cid): ## clan id to clan name
    with psycopg2.connect(adress) as conn:
        cursor=conn.cursor()
        statement="""SELECT clanname FROM clans WHERE id=%s"""
        cursor.execute(statement,(cid,))
        line=cursor.fetchone()
        return str(line[0]) 
    
def usernametoclanid(username):## user's clan id
    with psycopg2.connect(adress) as conn:
        cursor=conn.cursor()
        statement="""SELECT clannumber FROM users WHERE username=%s"""
        cursor.execute(statement,(username,))
        line=cursor.fetchone()
        return line[0]


def identify(pid): ## define type of problem
    with psycopg2.connect(adress) as conn:
        cursor=conn.cursor()
        statement="""SELECT *FROM problems WHERE id=%s"""
        cursor.execute(statement,(pid,))
        line=cursor.fetchone()
        print(len(line))
        if line[10] == 'general':
            return False
        elif line[10] == 'clan':
            return True
    
def DeleteUser(username):## delete user and his/her problems
    with psycopg2.connect(adress) as conn:
        cursor=conn.cursor()
        statement="""SELECT *FROM problems WHERE user_id=%s"""
        cursor.execute(statement,(UserNameToId(username),))
        line= cursor.fetchall()
        for i in line:
            delRelatedAnswers(i[1])
    with psycopg2.connect(adress) as conn:
        cursor=conn.cursor()
        statement="""DELETE FROM users WHERE username=%s"""
        cursor.execute(statement,(username,))

def delUser(user_id): ## delete user with user id
    DeleteUser(idToUserName(user_id))


def readMesssages(problem_id): ## read prblem related messages
     with psycopg2.connect(adress) as conn:
        cursor=conn.cursor()
        statement="""SELECT *FROM messages WHERE problem_id=%s"""
        cursor.execute(statement,(problem_id,))
        line=cursor.fetchall()
        return line  

def getAvatarPath(user_id): ## return avatar adress
    with psycopg2.connect(adress) as conn:
        cursor=conn.cursor()
        statement="""SELECT avatarpath FROM users WHERE id=%s"""
        cursor.execute(statement,(user_id,))
        line=cursor.fetchone()
        return str(line[0]) 
    
def Path(mid): ## return path of image adresss in messages
    with psycopg2.connect(adress) as conn:
        cursor=conn.cursor()
        statement="""SELECT imagepath FROM messages WHERE message_id=%s"""
        cursor.execute(statement,(mid,))
        line=cursor.fetchone()
        print(str(line[0]))
        return line[0]
    
def admincheck(var): ## check admin or not
     with psycopg2.connect(adress) as conn:
        cursor=conn.cursor()
        statement="""SELECT *FROM users WHERE username=%s"""
        cursor.execute(statement,(session['user'],))
        result=cursor.fetchone()
        print(result[8])
        if result[8] == var or result[8]=='general':
        
            return True
        else:
            return False
    
def getMessage(message_id): ## select specific messages
    with psycopg2.connect(adress) as conn:
        cursor=conn.cursor()
        statement="""SELECT message FROM messages WHERE message_id=%s"""
        cursor.execute(statement,(message_id,))
        line=cursor.fetchone()
        return str(line) 
  
def setReply(form,part):
    form.repliedMessageId=part
    print(form.repliedMessageId)

def checkAutorized(userid):## check user id in session
    if session['user'] == idToUserName(userid):
        return True
    else:
        return False
def log():
    if 'user' in session:
        return True
    else:
        return False
def delRelatedAnswers(qid): ## delete related messages for problem id
    with psycopg2.connect(adress) as conn:
        cursor=conn.cursor()
        statement="""UPDATE messages SET replyof=%s , clan_id=%s WHERE problem_id=%s"""
        cursor.execute(statement,(None,None,qid))
        
    with psycopg2.connect(adress) as conn:
        cursor=conn.cursor()
        statement="""DELETE FROM messages WHERE problem_id=%s"""
        cursor.execute(statement,(qid,))
 

def userClanId(): ## return clan id of user
   with psycopg2.connect(adress) as conn:
        cursor=conn.cursor()
        statement="""SELECT clannumber FROM users  WHERE username=%s"""
        cursor.execute(statement,(session['user'],))
        result=cursor.fetchone() 
        return result[0]
    
def makeAdmin(var,user_id): ### make user admin.
    a=2
    with psycopg2.connect(adress) as conn:
        cursor=conn.cursor()
        statement="""SELECT adminof FROM users  WHERE id=%s"""
        cursor.execute(statement,(user_id,))
        result=cursor.fetchone()
        if result[0] == 'general':
            a=1
    print('132113131313132123121231545645464654')
    if 'user' in session and admincheck(var)==True and a==2:
        print(4444444)
        with psycopg2.connect(adress) as conn:
            cursor=conn.cursor()
            statement="""UPDATE users SET adminof=%s WHERE adminof=%s"""
            cursor.execute(statement,(None,var))
        with psycopg2.connect(adress) as conn:
            cursor=conn.cursor()
            statement="""UPDATE users SET adminof=%s WHERE id=%s"""
            cursor.execute(statement,(var,user_id))
            print('here')

def checkClan(username,clan_id): ## clan member or not
    with psycopg2.connect(adress) as conn:
        cursor=conn.cursor()
        statement="""SELECT *FROM users WHERE username=%s AND clannumber=%s"""
        cursor.execute(statement,(username,clan_id))
        result=cursor.fetchone()
        if result:
            return True
        else:
            return False
        
        
def checkTime(qid): ## problem time exceed or not
    with psycopg2.connect(adress) as conn:
        cursor=conn.cursor()
        statement="""SELECT *FROM problems WHERE id=%s"""
        cursor.execute(statement,(qid,))
        result=cursor.fetchone()
        print(result[9])
        print('fwerger')
        print(type(result[9]))
        date_time= datetime.datetime.strptime(str(result[2]), '%Y-%m-%d %H:%M:%S.%f')
        print(date_time)
        if result[9]=='1d':
            date_time=date_time+timedelta(hours=24)
        elif result[9]=='2d':
            date_time=date_time+timedelta(hours=48)
        elif result[9]=='3d':
            date_time=date_time+timedelta(hours=72)
        elif result[9]=='4d':
            date_time=date_time+timedelta(hours=96)
        
        if date_time>datetime.datetime.now():
            return True
        else:
            return False
def lastActivitiesClan(clan_id): ## return last 5 activities of clan (messages ,problems)
     mes=[]
     prob=[]
     pack=[]
     empty=[0,0,"0"]
     indexProblem=0
     indexMessage=0
     with psycopg2.connect(adress) as conn:
         cursor=conn.cursor()
         statement="""SELECT *FROM problems WHERE clan_id=%s and typeof=%s ORDER BY senddate DESC LIMIT 5"""
         cursor.execute(statement,(clan_id,"clan"))
         prob=cursor.fetchall()
     with psycopg2.connect(adress) as conn:
         cursor=conn.cursor()
         statement="""SELECT *FROM messages WHERE clan_id=%s ORDER BY sendtime DESC LIMIT 5"""
         cursor.execute(statement,(clan_id,))
         mes=cursor.fetchall()
     
     act=len(mes)+len(prob) 
     if act>5:
         act=5
     print("mes ")
     print(len(mes))
     print("prob ")
     print(len(prob))
     t=0
     print('nein')
     if len(prob)==0 and len(mes)!=0:
         while t<act:
             pack.append(mes[indexMessage])
             indexMessage=indexMessage+1
             t=t+1
     elif len(mes)==0 and len(prob)!=0:
         while t<act:
             pack.append(prob[indexProblem])
             indexProblem=indexProblem+1
             t=t+1
             print(t)
        
     elif len(mes)!=0 and len(prob)!=0:
         while t<act:
             print(t)
             if str(prob[indexProblem][2])<=str(mes[indexMessage][2]):
                 pack.append(mes[indexMessage])
                 indexMessage=indexMessage+1
                 if(indexMessage==len(mes)):
                     mes.append(empty)
                     print('e1')
             elif str(prob[indexProblem][2])>str(mes[indexMessage][2]):
                 pack.append(prob[indexProblem])
                 indexProblem=indexProblem+1  
                 if indexProblem==len(prob):
                     prob.append(empty)
             t=t+1
     print('tkkk')
     print(len(pack))
     return pack
         
def delRelatedBets(problem_id):## deletes related bets with problem_id
    with psycopg2.connect(adress) as conn:
        cursor=conn.cursor()
        statement="""DELETE FROM bets WHERE question_id=%s"""
        cursor.execute(statement,(problem_id,))
        
def lastActivities(user_pack):## get last 5 activities of user(message or problem)
    prob=[]
    mes=[]
    pack=[]
    empty=[0,0,"0"]
    indexProblem=0
    indexMessage=0
    with psycopg2.connect(adress) as conn:
        cursor=conn.cursor()
        statement="""SELECT *FROM users WHERE username=%s"""
        cursor.execute(statement,(session['user'],))
        result=cursor.fetchone()
    if result[6]==user_pack[6]:
        with psycopg2.connect(adress) as conn:
            cursor=conn.cursor()
            statement="""SELECT *FROM problems WHERE user_id=%s ORDER BY senddate DESC LIMIT 5"""
            cursor.execute(statement,(user_pack[0],))
            prob=cursor.fetchall()
            
        with psycopg2.connect(adress) as conn:
            cursor=conn.cursor()
            statement="""SELECT *FROM messages WHERE user_id=%s ORDER BY sendtime DESC LIMIT 5"""
            cursor.execute(statement,(user_pack[0],))
            mes=cursor.fetchall()
    else:
        with psycopg2.connect(adress) as conn:
            cursor=conn.cursor()
            statement="""SELECT *FROM problems WHERE user_id=%s AND typeof=%s ORDER BY senddate DESC LIMIT 5"""
            cursor.execute(statement,(user_pack[0],"general"))
            prob=cursor.fetchall()
            
        with psycopg2.connect(adress) as conn:
            cursor=conn.cursor()
            statement="""SELECT *FROM messages WHERE user_id=%s AND  NOT clan_id=%s ORDER BY sendtime DESC LIMIT 5"""
            cursor.execute(statement,(user_pack[0],user_pack[6]))
            mes=cursor.fetchall()
    act=len(mes)+len(prob) 
    if act>5:
        act=5
    print("mes ")
    print(len(mes))
    print("prob ")
    print(len(prob))
    t=0
    if len(prob)==0 and len(mes)!=0:
        while t<act:
            pack.append(mes[indexMessage])
            indexMessage=indexMessage+1
            t=t+1
    elif len(mes)==0 and len(prob)!=0:
        while t<act:
            pack.append(prob[indexProblem])
            indexProblem=indexProblem+1
            t=t+1
        
    elif len(mes)!=0 and len(prob)!=0:
        while t<act:
            print(t)
            if str(prob[indexProblem][2])<=str(mes[indexMessage][2]):
                pack.append(mes[indexMessage])
                indexMessage=indexMessage+1
                if(indexMessage==len(mes)):
                    mes.append(empty)
                    print('e1')
            elif str(prob[indexProblem][2])>str(mes[indexMessage][2]):
                pack.append(prob[indexProblem])
                indexProblem=indexProblem+1  
                if indexProblem==len(prob):
                    prob.append(empty)
            t=t+1
    print('tkkk')
    print(len(pack))
    return pack
            
@app.route('/makeadmin/<vari>/<user_id>',methods=['GET','POST'])
def makeadmin(vari,user_id): ## succesfully admin assigned
    return render_template('success.html',func=makeAdmin,vari=vari,user_id=user_id)
            
        


      
@app.route('/editMessage/<problem_id>/<message_id>',methods=['GET','POST'])
def editMessage(problem_id,message_id): ## message edit url
    form=editMessageForm()
    with psycopg2.connect(adress) as conn:
        cursor=conn.cursor()
        statement="""SELECT *FROM messages WHERE message_id=%s"""
        cursor.execute(statement,(message_id,))                   ## read message and prepopulate areas.
        line=cursor.fetchone()
        pack=line
        if form.validate_on_submit():
            with psycopg2.connect(adress) as conn:
                cursor=conn.cursor()
                statement="""UPDATE messages SET message=%s WHERE message_id=%s"""
                cursor.execute(statement,(str(form.message.data),message_id))
            
    return render_template('editMessage.html',pack=pack,form=form,func=userClanId)
    
@app.route('/',methods=['GET','POST']) 
def home(): ## main page url
    key=''
    if 'user' not in session: ## login or not
        key="no"
    else:
        key="yes"
    
    with psycopg2.connect(adress) as conn: ## last 10 problems best 10 user best 10 clan 
        cursor=conn.cursor()
        statement="""SELECT *FROM problems WHERE typeof=%s ORDER BY senddate DESC LIMIT 10;"""
        cursor.execute(statement,("general",))
        line=cursor.fetchall()
        
    with psycopg2.connect(adress) as conn:
        cursor=conn.cursor()
        statement="""SELECT *FROM users ORDER BY points DESC LIMIT 10 """
        cursor.execute(statement)
        line2=cursor.fetchall()
        
    with psycopg2.connect(adress) as conn:
        cursor=conn.cursor()
        statement="""SELECT *FROM clans ORDER BY points DESC LIMIT 10 """
        cursor.execute(statement)
        line3=cursor.fetchall()
        
    return render_template('main.html',line=line,line2=line2,line3=line3,key=key)


@app.route('/delete/<qid>',methods=['GET','POST'])
def deleteQuestion(qid): ## delete question url
    delRelatedAnswers(qid)
    delRelatedBets(qid)
    with psycopg2.connect(adress) as conn:
        cursor=conn.cursor()
        statement="""DELETE FROM problems WHERE id=%s"""
        cursor.execute(statement,(qid,))
    return redirect(url_for('writer')) 
 
@app.route('/deleteMessage/<pid>/<mid>',methods=['GET','POST'])
def deleteMessage(pid,mid): ## delete message url
    with psycopg2.connect(adress) as conn:
        cursor=conn.cursor()
        statement="""SELECT *FROM messages WHERE replyof=%s"""
        cursor.execute(statement,(mid,))
        line=cursor.fetchall()
        if line:
            for i in line:
                with psycopg2.connect(adress) as conn: ## if is replied , to not break ref. integrity reply of maken none.
                    cursor=conn.cursor()
                    statement="""UPDATE messages SET replyof=%s , clan_id=%s WHERE replyof=%s"""
                    cursor.execute(statement,(None,None,mid))
        
    with psycopg2.connect(adress) as conn:
        cursor=conn.cursor()
        statement="""SELECT clannumber FROM users WHERE username=%s"""
        cursor.execute(statement,(session['user'],))
        result=cursor.fetchone()
        
    with psycopg2.connect(adress) as conn:
        cursor=conn.cursor()
        statement="""DELETE FROM messages WHERE message_id=%s"""
        cursor.execute(statement,(mid,))
    
    if identify(pid)==True:  ## define we delete clan mesage or genaral message accordin to that we will redirected.
        return redirect(url_for('clanDiscuss',clan_id=result[0],topic_id=line[1],reply=str(0)))
    else:
        return redirect(url_for('problems',var=pid,reply=0))   
@app.route('/seeClan/<clan_id>',methods=['GET','POST'])
def seeClan(clan_id): ## see all clan activities
    x = usernametoclanid(session['user'])
    if int(x)==int(clan_id):
        with psycopg2.connect(adress) as conn:
            cursor=conn.cursor()
            statement="""SELECT *FROM problems WHERE clan_id=%s ORDER BY senddate DESC"""
            cursor.execute(statement,(clan_id,))
            result=cursor.fetchall()
            return render_template("see.html",la=result)
    else:
        print('dfasdfasdf')
        print(clan_id)
        print(usernametoclanid(session['user']))
        return redirect(url_for('clans',clan_id=clan_id))
    
@app.route('/seeAll/<typ>',methods=['GET','POST'])
def seeAll(typ): ## see all topic problems according parameter typ
    with psycopg2.connect(adress) as conn:
        cursor=conn.cursor()
        statement="""SELECT *FROM problems WHERE topic=%s ORDER BY senddate DESC"""
        cursor.execute(statement,(typ,))
        result=cursor.fetchall()
        return render_template("see.html",la=result,key=1)

@app.route('/reportMessage/<typ>/<mid>/<pid>',methods=['GET','POST'])
def reportMessage(mid,pid,typ):## increse reportnum of message 
    if 'user' in session:
        with psycopg2.connect(adress) as conn:
            cursor=conn.cursor()
            statement="""UPDATE messages SET reportnum=reportnum+1 WHERE message_id=%s and problem_id=%s"""
            cursor.execute(statement,(mid,pid))
            if typ == 'g':
                return redirect(url_for('problems',var=pid,reply=0))
            elif typ=='c':
                with psycopg2.connect(adress) as conn:
                    cursor=conn.cursor()
                    statement="""SELECT clan_id FROM messages WHERE message_id=%s problem_id=%s"""
                    cursor.execute(statement,(mid,pid))
                    line=cursor.fetchone()
                
                return redirect(url_for('clan',clan_id=line[0],topic_id=pid,reply=0))
    else:
        return redirect(url_for('login'))
@app.route('/editQuestion/<qid>',methods=['GET','POST'])
def editQuestion(qid): ## edit question url
    form=PostForm()
    with psycopg2.connect(adress) as conn:
        cursor=conn.cursor()
        statement="""SELECT *FROM problems WHERE id=%s"""
        cursor.execute(statement,(qid,))
        line=cursor.fetchone()
        pack=list(line)
        print(len(line))
        if form.validate_on_submit():
            print('hasdfeer')
            with psycopg2.connect(adress) as conn:
                cursor=conn.cursor()
                statement="""UPDATE problems SET title=%s,topic=%s,giventime=%s,question=%s,answer=%s WHERE id=%s""" ## pre populate some field
                cursor.execute(statement,(str(form.title.data),str(form.topic.data),str(form.time.data),str(form.question.data),form.answer.data,qid))
                print('updated')
                
        else:
            print(4444)
            for error in form.errors.items():
                print(error)
        return render_template('editor.html',form=form,pack=pack,func=userClanId)
    
@app.route("/terms",methods=['GET'])
def terms(): ## terms url
    return render_template('terms.html')

@app.route("/faq",methods=['GET'])
def faq(): ## faq url
    return render_template('faq.html')
@app.route("/signup",methods=['GET','POST'])
def signup(): ## sign up url
    if 'user' in session: ##  if user in session already redirect him/her user page.
        return redirect(url_for('user',var=UserNameToId(session['user'])))
    

    print(os.path.join(app.config['UPLOAD_FOLDER']),file=sys.stderr) ## upload folder for avatar
    sys.stderr.flush()
    form = SignUpForm()
    if form.validate_on_submit():
        print('no')
        crypt=hasher.hash(form.password1.data)   ## encrypt password with sha-256
        try:
            conn=psycopg2.connect(adress)
            f = form.upload.data
            filename = secure_filename(f.filename)
            print(filename)
            filename = filename+str(datetime.datetime.utcnow()) ## unique file name
            print(filename)
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename)) ## save avatar
            cursor=conn.cursor()
            #print(crypt)
            statement="""INSERT INTO users(username,pass_word,avatarpath,email,isActive)
            VALUES(%s,%s,%s,%s,TRUE)"""
            cursor.execute(statement,(str(form.username.data),str(crypt),str(filename),str(form.email1.data)))
            conn.commit()
            cursor.close()
        except psycopg2.DatabaseError as e:
            print(e.args[0])
            os.remove("static/avatars/"+filename)
            if "username" in e.args[0]:
                conn.rollback()
                conn.close()
                return render_template('home.html', form=form,errorU="The username  is already in use") ## some validation errors begins
            elif "email" in e.args[0]:
                conn.rollback()
                conn.close()
                return render_template('home.html', form=form,errorE="The email address is already in use")
        finally:
            conn.close()
        
        
        try:
            conn=psycopg2.connect(adress)
            cursor=conn.cursor()
            statement="""SELECT *FROM users WHERE username=%s"""
            cursor.execute(statement,(form.username.data,))
            line=cursor.fetchone()
            conn.commit()
            cursor.close()
        except psycopg2.DatabaseError as e:
            conn.rollback()
        finally:
            conn.close()
            
        
        print(form.username.data,file=sys.stderr)
        sys.stderr.flush()
        session['user']=form.username.data
        ##isActive
        try:
            conn=psycopg2.connect(adress)
            cursor=conn.cursor()
            statement="""UPDATE users SET isActive=TRUE WHERE username=%s"""
            cursor.execute(statement,(form.username.data,))
            conn.commit()
            cursor.close()
        except psycopg2.DatabaseError as e:
            conn.rollback()
        finally:
            conn.close()
        
        return redirect(url_for('user',var=line[0]))
    else:
        print('failed')
    return render_template('home.html', form=form)

@app.route('/problems/<var>/<reply>',methods=['GET','POST'])
def problems(var,reply): ## problems page url                  ## this become a bit complicated at the end.
    print('hew')
    print(reply)
    r = reply
    htmlPart1="""<div class="quate"><p font size="6" font style>quote</p>""" ## quate html stuff
    htmlPart2="</div><br>"
    key='yes'
    show=True
    
    try:
        conn=psycopg2.connect(adress)
        cursor=conn.cursor()
        statement="""SELECT *FROM problems WHERE id=%s"""
        cursor.execute(statement,(var,))
        line=cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()          
    except psycopg2.DatabaseError as e:
        conn.rollback()
    finally:
        conn.close()
    if 'user' not in session:
        key='no' ## if user not in session soft article wil. loade.
        return render_template("softarticle.html",variable=line,messages=readMesssages(var),func=getAvatarPath,funcid=idToUserName,reply=reply,check=checkAutorized,log=log,path=Path,key=key)
    with psycopg2.connect(adress) as conn:
        cursor=conn.cursor()
        statement="""SELECT *FROM users WHERE username=%s"""
        cursor.execute(statement,(session['user'],))
        result=cursor.fetchone()
        
    with psycopg2.connect(adress) as conn:
        cursor=conn.cursor()
        statement="""SELECT *FROM clans WHERE id=%s"""
        cursor.execute(statement,(result[6],))
        result2=cursor.fetchone()
    
    with psycopg2.connect(adress) as conn:
        cursor=conn.cursor()
        statement="""SELECT *FROM bets WHERE question_id=%s"""
        cursor.execute(statement,(var,))
        res=cursor.fetchall()
    boolForm=True ## boolForm means we can render bet form.
    for i in res:  ## if user send bet before try to block user to do it again
        if i[6]==var and (i[1]==UserNameToId(session['user']) or i[5]==userClanId(session['user'])):
            boolForm=False
        
    if  usernametoclanid(idToUserName(line[0]))==usernametoclanid(session['user']): ## if clan id are same block user to send bet.
        boolForm=False
        show=False
    
    t=checkTime(line[1]) 
    print('here')
    print(line[7])
    print(result[0])
    
    
    if line[7]==False and t==True and line[0]!=result[0] and boolForm is not False: ## times up or not
        boolForm=True
    elif boolForm is not False:
        boolForm=False             ## if right answer comes, delete older wrong answers if exist.
        with psycopg2.connect(adress) as conn:
            cursor=conn.cursor()
            statement="""SELECT *FROM bets WHERE question_id=%s"""
            cursor.execute(statement,(line[1],))
            result3=cursor.fetchall()
            if result3:
                for i in result3:
                    if i[1]:                      
                        with psycopg2.connect(adress) as conn:
                            cursor=conn.cursor()
                            statement="""UPDATE users SET points=points+%s WHERE id=%s"""
                            cursor.execute(statement,(int(i[2])*3,i[1]))
                    elif i[5]:
                        with psycopg2.connect(adress) as conn:
                            cursor=conn.cursor()
                            statement="""UPDATE clans SET points=points+%s WHERE id=%s"""
                            cursor.execute(statement,(int(i[2])*3,i[5]))
                    with psycopg2.connect(adress) as conn:
                        cursor=conn.cursor()
                        statement="""UPDATE problems SET isanswered=%s WHERE id=%s"""
                        cursor.execute(statement,(True,i[6]))
                    break
                            
                with psycopg2.connect(adress) as conn:
                    cursor=conn.cursor()
                    statement="""DELETE FROM bets  WHERE id=%s"""
                    cursor.execute(statement,(i[0],))
        
    if line:
        if 'user' in session:
            pack=list(line)
            form=LeaveReply()
            form2=answerForm()
            if form2.validate_on_submit():
                
                with psycopg2.connect(adress) as conn2:
                        cursor2=conn2.cursor()
                        if int(form2.amount.data) <= result[5]:
                            if form2.radio.data == 'individual':  ## in behalf of myself
                                statement2="""INSERT INTO bets(user_id,amount,typeof,answer,question_id) VALUES(%s,%s,%s,%s,%s)"""
                                cursor2.execute(statement2,(UserNameToId(session['user']),form2.amount.data,form2.radio.data,form2.answer.data,line[1]))
                                print(212131321312312312313213213131131132131)
                                print(line[1])
                                with psycopg2.connect(adress) as conn:
                                    cursor=conn.cursor()
                                    statement="""UPDATE users SET points=%s WHERE id=%s""" ## point excluded
                                    cursor.execute(statement,(result[5]-int(form2.amount.data),UserNameToId(session['user'])))
                                    
                                with psycopg2.connect(adress) as conn: ## totoal collected points increased
                                    cursor=conn.cursor()
                                    statement="""UPDATE problems SET totalcollectedpoints=totalcollectedpoints+%s WHERE id=%s"""
                                    cursor.execute(statement,(int(form2.amount.data),line[1]))
                                    
                                with psycopg2.connect(adress) as conn: ##
                                    cursor=conn.cursor()
                                    statement="""SELECT *FROM problems WHERE id=%s"""
                                    cursor.execute(statement,(line[1],))
                                    snc = cursor.fetchone()
                                print('neden buraya girmiyor')
                                if float(form2.answer.data) == snc[6]: ## set isanswered true if answer true
                                    with psycopg2.connect(adress) as conn:
                                        cursor=conn.cursor()
                                        statement="""UPDATE problems SET isAnswered=TRUE WHERE id=%s"""
                                        cursor.execute(statement,(line[1],))
                                
                        elif form2.radio.data == 'individual':
                            error="Amount of Bet Can Not be More Than Your Points!"
                            return render_template("article.html",variable=pack,messages=readMesssages(var),func=getAvatarPath,funcid=idToUserName,form=form,func3=setReply,reply=reply,check=checkAutorized,log=log,path=Path,answerform=form2,err=error,boolForm=boolForm,show=show)
                       
                        if result2 is not None: ## clan answers handle begins
                            if int(form2.amount.data) <= result2[2]:
                                if form2.radio.data == 'clan':
                                    if result[10] == True:
                                        statement2="""INSERT INTO bets(clan_id,amount,typeof,answer,question_id) VALUES(%s,%s,%s,%s)"""
                                        cursor2.execute(statement2,(usernametoclanid(session['user']),form2.amount.data,form2.radio.data,form2.answer.data,line[1]))
                                        
                                        with psycopg2.connect(adress) as conn:
                                            cursor=conn.cursor()
                                            statement="""UPDATE clans SET points=%s WHERE id=%s"""
                                            cursor.execute(statement,(result2[2]-int(form2.amount.data),usernametoclanid(session['user'])))
                                            
                                        with psycopg2.connect(adress) as conn:
                                            cursor=conn.cursor()
                                            statement="""UPDATE problems SET totalcollectedpoints=totalcollectedpoints+%s WHERE id=%s"""
                                            cursor.execute(statement,(int(form2.amount.data),line[1]))
                                        
                                    else:
                                        error="You Are Not Authorized"
                                        return render_template("article.html",variable=pack,messages=readMesssages(var),func=getAvatarPath,funcid=idToUserName,form=form,func3=setReply,reply=reply,check=checkAutorized,log=log,path=Path,answerform=form2,err=error,boolForm=boolForm,show=show)
                                        
                            elif form2.radio.data == 'clan':
                                error="Amount of Bet Can Not be More Than Points of Clan!"
                                return render_template("article.html",variable=pack,messages=readMesssages(var),func=getAvatarPath,funcid=idToUserName,form=form,func3=setReply,reply=reply,check=checkAutorized,log=log,path=Path,answerform=form2,err=error,boolForm=boolForm,show=show)
                                
            if reply is not 0:
                form.repliedMessageId=r
                print(999)
                print(r)
            if form.validate_on_submit(): ## message form related stuff begins
                f = form.upload.data
                if f is not None:
                    filename = secure_filename(f.filename)
                    filename = filename+str(datetime.datetime.utcnow())   ### if image loaded secure filename created and saved.
                    f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                if r > str(0):
                    print('here')
                    print(r)
                    sub=getMessage(form.repliedMessageId)[2:len(getMessage(form.repliedMessageId))-3]  ## html script created on jinja with |safe block it is converted.
                    x=htmlPart1+sub+htmlPart2+"<p>"+form.message.data+"</p>"
                    with psycopg2.connect(adress) as conn2:
                        if f is not None: ## if reply of something
                            cursor2=conn2.cursor()
                            statement2="""INSERT INTO messages(user_id,message,replyof,problem_id,typeofmessage,containanswer,imagepath) VALUES(%s,%s,%s,%s,%s,%s,%s)"""
                            cursor2.execute(statement2,(UserNameToId(session['user']),x,form.repliedMessageId,line[1],"general",form.spoiler.data,str(filename)))
                        else:
                            cursor2=conn2.cursor()
                            statement2="""INSERT INTO messages(user_id,message,replyof,problem_id,typeofmessage,containanswer) VALUES(%s,%s,%s,%s,%s,%s)"""
                            cursor2.execute(statement2,(UserNameToId(session['user']),x,form.repliedMessageId,line[1],"general",form.spoiler.data))
                            
                else: ## not reply of something
                    
                    
                    with psycopg2.connect(adress) as conn2:
                        print(form.message.data)
                        cursor2=conn2.cursor()
                        if f is not None:
                            statement2="""INSERT INTO messages(user_id,message,problem_id,typeofmessage,containanswer,imagepath) VALUES(%s,%s,%s,%s,%s,%s)"""
                            cursor2.execute(statement2,(UserNameToId(session['user']),form.message.data,line[1],"general",form.spoiler.data,str(filename)))
                            print("herer")
                        else:
                            statement2="""INSERT INTO messages(user_id,message,problem_id,typeofmessage,containanswer) VALUES(%s,%s,%s,%s,%s)"""
                            cursor2.execute(statement2,(UserNameToId(session['user']),form.message.data,line[1],"general",form.spoiler.data))
                            
     
                        
        print('cikis')
        return render_template("article.html",variable=pack,messages=readMesssages(var),func=getAvatarPath,funcid=idToUserName,form=form,func3=setReply,reply=reply,check=checkAutorized,log=log,path=Path,answerform=form2,boolForm=boolForm,show=show)  ## render article with some functions and lists.




@app.route('/clanDiscuss/<clan_id>/<topic_id>/<reply>',methods=['GET','POST'])
def clanDiscuss(clan_id,topic_id,reply): ##clan discuss page. nearly same as problems
    htmlPart1="""<div class="quate"><p font size="6" font style>quote</p>"""
    htmlPart2="</div><br>"
    form=LeaveReply()
    with psycopg2.connect(adress) as conn:
        cursor=conn.cursor()
        statement="""SELECT *FROM problems WHERE id=%s AND typeof=%s"""
        cursor.execute(statement,(topic_id,'clan'))
        result=cursor.fetchone()
        r=reply
        if result:
            
            if reply is not 0:
                form.repliedMessageId=reply
                print(999)
                print(r)
            if form.validate_on_submit():
                f = form.upload.data
                if f is not None:
                    filename = secure_filename(f.filename)
                    filename = filename+str(datetime.datetime.utcnow())
                    f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                if r > str(0):
                    print('here')
                    print(r)
                    sub=getMessage(form.repliedMessageId)[2:len(getMessage(form.repliedMessageId))-3]
                    x=htmlPart1+sub+htmlPart2+"<p>"+form.message.data+"</p>"
                    with psycopg2.connect(adress) as conn2:
                        if f is not None:
                            cursor2=conn2.cursor()
                            statement2="""INSERT INTO messages(user_id,message,replyof,problem_id,typeofmessage,containanswer,imagepath) VALUES(%s,%s,%s,%s,%s,%s,%s)"""
                            cursor2.execute(statement2,(UserNameToId(session['user']),x,form.repliedMessageId,result[1],"clan",form.spoiler.data,str(filename)))
                        else:
                            cursor2=conn2.cursor()
                            statement2="""INSERT INTO messages(user_id,message,replyof,problem_id,typeofmessage,containanswer) VALUES(%s,%s,%s,%s,%s,%s)"""
                            cursor2.execute(statement2,(UserNameToId(session['user']),x,form.repliedMessageId,result[1],"clan",form.spoiler.data))
                            
                else:
                    
                    
                    with psycopg2.connect(adress) as conn2:
                        print(form.message.data)
                        cursor2=conn2.cursor()
                        if f is not None:
                            statement2="""INSERT INTO messages(user_id,message,problem_id,typeofmessage,containanswer,imagepath) VALUES(%s,%s,%s,%s,%s,%s)"""
                            cursor2.execute(statement2,(UserNameToId(session['user']),form.message.data,result[1],"clan",form.spoiler.data,str(filename)))
                            print("herer")
                        else:
                            statement2="""INSERT INTO messages(user_id,message,problem_id,typeofmessage,containanswer) VALUES(%s,%s,%s,%s,%s)"""
                            cursor2.execute(statement2,(UserNameToId(session['user']),form.message.data,result[1],"clan",form.spoiler.data))
                    
                    
                
        
    
    return render_template('discuss.html',result=result,messages=readMesssages(topic_id),funcid=idToUserName,func=getAvatarPath,form=form,func3=setReply,reply=reply,check=checkAutorized,log=log,path=Path,clan_id=clan_id)

    
@app.route('/writer',methods=['GET','POST'])
def writer(): ## creates form for writing problems.
    print(5)
    if 'user' in session:
        print(UserNameToId(session['user']))
        print(999)
        form = PostForm()
        if form.validate_on_submit():
            print("heer")
            print(session['user'])
            with psycopg2.connect(adress) as conn:
                cursor=conn.cursor()            
                statement="""INSERT INTO problems(user_id,title,question,totalcollectedpoints,answer,topic,giventime,typeof) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""
                
                cursor.execute(statement,(UserNameToId(session['user']),str(form.title.data),str(form.question.data),0,str(form.answer.data),str(form.topic.data),str(form.time.data),'general'))
                
            
            try:
                conn=psycopg2.connect(adress)
                cursor=conn.cursor()
                statement="""SELECT *FROM problems WHERE user_id=%s AND title=%s AND topic=%s """
                cursor.execute(statement,(UserNameToId(session['user']),form.title.data,form.topic.data))
                line=cursor.fetchone()
                conn.commit()
                cursor.close()
            except psycopg2.DatabaseError as e:
                conn.rollback()
            finally:
                conn.close()   
                
            if line:
                pack=list(line)
                return redirect(url_for('problems',var=pack[1],reply=str(0)))
                
        else:
            for error in form.topic.errors:
                print(error)      
        return render_template('writer.html',form=form)
        
    else:
         
         return redirect(url_for('login'))   ## user not in session


@app.route('/clanWriter/<clan_id>',methods=['GET','POST'])
def clanWriter(clan_id):  ## disquss cretor. nearly same as writer.
    if checkClan(session['user'],clan_id) == True:
        form = PostForm()
        if form.validate_on_submit():
            print("heer")
            print(session['user'])
            with psycopg2.connect(adress) as conn:
                cursor=conn.cursor()            
                statement="""INSERT INTO problems(user_id,title,question,totalcollectedpoints,answer,topic,giventime,typeof,clan_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
                
                cursor.execute(statement,(UserNameToId(session['user']),str(form.title.data),str(form.question.data),0,str(form.answer.data),str(form.topic.data),str(form.time.data),'clan',clan_id))
                
            
            try:
                conn=psycopg2.connect(adress)
                cursor=conn.cursor()
                statement="""SELECT *FROM problems WHERE user_id=%s AND title=%s AND topic=%s """
                cursor.execute(statement,(UserNameToId(session['user']),form.title.data,form.topic.data))
                line=cursor.fetchone()
                conn.commit()
                cursor.close()
            except psycopg2.DatabaseError as e:
                conn.rollback()
            finally:
                conn.close() 
            
            
            if line:
                return redirect(url_for('clanDiscuss',clan_id=clan_id,topic_id=line[1],reply=str(0)))
        else:
            return render_template('writer.html',form=form,clan_id=clan_id)
    else:
        return redirect(url_for('clans',clan_id=clan_id),error='You are not a member of this clan.')
@app.route("/login",methods=['GET','POST'])
def login(): ## login mechanism
    if 'user' in session:
        return redirect(url_for('user',var=UserNameToId(session['user']))) ## if it is in sesion already  redirect user page
    form = LoginForm()
    if form.validate_on_submit():
        with psycopg2.connect(adress) as conn:
            print('JA')
            cursor=conn.cursor()
            
            
            statement="""SELECT pass_word FROM users WHERE username=%s"""
            cursor.execute(statement,(str(form.username.data),))
            data = cursor.fetchone()
            print(str(form.username.data))
            if data is not None:
                
                statement2="""SELECT *FROM users WHERE username=%s"""
                cursor.execute(statement2,(form.username.data,))
                line=cursor.fetchone()
                
                print(data[0])
                if hasher.verify(str(form.password.data),data[0]) is True: ## is password correct
                    statement2="""UPDATE users SET isActive=TRUE WHERE username=%s """
                    cursor.execute(statement2,(form.username.data,))
                    session['user']=form.username.data
                    return redirect(url_for('user',var=line[0]))
                else:
                    return render_template('login.html',form=form,error=noUsernamePasswordFound)
            
            else:
                return render_template('login.html',form=form,error=noUsernamePasswordFound)
            
    return render_template('login.html',form=form,error='')


@app.route('/logout',methods=['GET','POST'])  
def logout():## logout url discharge session redirect to login
    if 'user' in session:
        try:
            conn=psycopg2.connect(adress)
            cursor=conn.cursor()
            statement="""UPDATE users SET isActive=FALSE WHERE username=%s """
            cursor.execute(statement,(session['user'],))
            conn.commit()
            cursor.close()
        except psycopg2.DatabaseError as e:
            conn.rollback()
        finally:
            conn.close()
        session.pop('user',None)
        return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))

@app.route ('/createClan',methods=['GET','POST'])  
def createClan(): ## cerate clan url. if user has not 100 points error will be thrown
    if 'user' in session:
        form=clanForm()
        if form.validate_on_submit():
            with psycopg2.connect(adress) as conn:
                cursor=conn.cursor()
                statement="""SELECT *FROM users WHERE username=%s"""
                cursor.execute(statement,(session['user'],))
                line=cursor.fetchone()
                if line[5] >= 1000:
                    with psycopg2.connect(adress) as conn:
                        cursor=conn.cursor()
                        statement="""INSERT INTO clans(headofclan,points,clanname) VALUES(%s,%s,%s)"""
                        cursor.execute(statement,(UserNameToId(session['user']),1000,form.clanName.data))
                    with psycopg2.connect(adress) as conn:
                        cursor=conn.cursor()
                        statement="""SELECT id FROM clans WHERE headofclan=%s"""
                        cursor.execute(statement,(UserNameToId(session['user']),))
                        line2=cursor.fetchone()
                    with psycopg2.connect(adress) as conn:
                        cursor=conn.cursor()
                        statement="""UPDATE users SET points=%s,clannumber=%s,headofclan=TRUE WHERE id=%s"""
                        cursor.execute(statement,(line[5]-1000,line2[0],UserNameToId(session['user'])))
                    return redirect(url_for('clans',clan_id=line2[0]))
                else:
                    error="To Create a Clan Your Points Must Be Greater Than 1000"
                    return render_template('clanform.html',error=error,form=form)
        return render_template('clanform.html',form=form)
    else:
        print('sdgdsfgdsx')
        return redirect(url_for('login'))

@app.route('/join/<clan>/<user>',methods=['GET','POST'])
def join(clan,user): ## join clan url
    with psycopg2.connect(adress) as conn:
        cursor=conn.cursor()
        statement="""SELECT *FROM users WHERE id=%s"""
        cursor.execute(statement,(user,))
        line=cursor.fetchone()
        
        if line[6]:
            return redirect(url_for('user',var=UserNameToId(session['user']),clanerr='You are already a clan member.')) ## if user is a clan member already
    
    with psycopg2.connect(adress) as conn: ##else
        cursor=conn.cursor()
        statement="""SELECT *FROM request WHERE user_id=%s"""
        cursor.execute(statement,(user,))
        line2=cursor.fetchone()
        
        if line2:
            return redirect(url_for('user',var=UserNameToId(session['user']),clanerr='You can not send multiple clan request.'))
   
    with psycopg2.connect(adress) as conn:
        cursor=conn.cursor()
        statement="""INSERT INTO request(user_id,clan_id) VALUES(%s,%s) """
        cursor.execute(statement,(user,clan))
        return redirect(url_for('user',var=UserNameToId(session['user']),clanerr='Join Request is Sent to the Head of Clan '))

@app.route('/accept/<user>/<clan>',methods=['GET','POST'])
def accept(user,clan):  ## accept to clan url delete request and accept
    with psycopg2.connect(adress) as conn:
        cursor=conn.cursor()
        statement="""DELETE FROM request WHERE user_id=%s """
        cursor.execute(statement,(user,))
    with psycopg2.connect(adress) as conn:
        cursor=conn.cursor()
        statement="""UPDATE users SET clannumber=%s WHERE id=%s"""
        cursor.execute(statement,(clan,user))      
        return redirect(url_for('user',var=UserNameToId(session['user']),clanerr='User Joined Clan'))    

@app.route('/deny/<user>',methods=['GET','POST'])
def deny(user): ## deny request 
    with psycopg2.connect(adress) as conn:
        cursor=conn.cursor()
        statement="""DELETE FROM request WHERE user_id=%s """
        cursor.execute(statement,(user,))
        return redirect(url_for('user',var=UserNameToId(session['user']),clanerr='User Denied to the Join Clan'))
 
@app.route('/clans/<clan_id>',methods=['GET','POST'])
def clans(clan_id): ## clan url nearly same as user page url
    if 'user' not in session:
        return redirect(url_for('login'))
    with psycopg2.connect(adress) as conn:
        cursor=conn.cursor()
        statement="""SELECT *FROM users WHERE username=%s"""
        cursor.execute(statement,(session['user'],))
        line2=cursor.fetchone()
    with psycopg2.connect(adress) as conn:
        cursor=conn.cursor()
        statement="""SELECT *FROM clans WHERE id=%s"""
        cursor.execute(statement,(clan_id,))
        line=cursor.fetchone()
        return render_template('clan.html',pack=line,line=line2,la=lastActivitiesClan(clan_id))
    
               
@app.route('/user/<var>', methods=['GET','POST'])
def user(var): ### user page url
    
    if 'user' not in session:
        return redirect(url_for('login'))
    print(type(var))
    
    messageHolder=[]
    messageHolder2=[]
    with psycopg2.connect(adress) as conn:
        cursor=conn.cursor()
        statement="""SELECT clannumber,headofClan FROM users WHERE username=%s"""
        cursor.execute(statement,(session['user'],))
        line9=cursor.fetchone()
    with psycopg2.connect(adress) as conn:
        cursor=conn.cursor()
        statement="""SELECT *FROM users WHERE id=%s"""
        cursor.execute(statement,(var,))
        lineq=cursor.fetchone()
        
    if checkAutorized(var) and line9[1]==True:  ## reported messages checked
        with psycopg2.connect(adress) as conn:
            cursor=conn.cursor()
            statement="""SELECT *FROM messages WHERE reportnum>=5 and typeofmessage=%s"""
            cursor.execute(statement,("clan",))
            admin2=cursor.fetchall()
        
        for i in admin2:
            if i[7]==line9[0]:
                messageHolder2.append(i)
        
    with psycopg2.connect(adress) as conn:
        cursor=conn.cursor()
        statement="""SELECT adminof FROM users WHERE username=%s"""
        cursor.execute(statement,(session['user'],))
        line0=cursor.fetchone()
    if checkAutorized(var)==True and (line0[0]=="ds" or line0[0]=="algo" or line0[0]=="m" or line0[0]=="phy"):  ## if user admin handle reports 
        print('laelile')
        with psycopg2.connect(adress) as conn:
            cursor=conn.cursor()
            statement="""SELECT *FROM messages WHERE reportnum>=5 and typeofmessage=%s"""
            cursor.execute(statement,("general",))
            admin=cursor.fetchall()
        
        print(len(admin))
        for i in admin:
            print(len(i))
            if(line0[0]=="ds" and typeDefiner(i)=="ds"):
                messageHolder.append(i)
            elif(line0[0]=="algo" and typeDefiner(i)=="algo"):
                messageHolder.append(i)
            elif(line0[0]=="m" and typeDefiner(i)=="m"):
                messageHolder.append(i)
            elif(line0[0]=="phy" and typeDefiner(i)=="phy"):
                messageHolder.append(i)
                
    if 'user' in session:
        try:
            conn=psycopg2.connect(adress)
            cursor=conn.cursor()
            statement="""SELECT *FROM users WHERE id=%s"""
            cursor.execute(statement,(var,))
            line=cursor.fetchone()
            conn.commit()
            cursor.close()
            conn.close()
            if line:
                with psycopg2.connect(adress) as conn:
                    cursor=conn.cursor()
                    statement="""SELECT adminof FROM users WHERE username=%s"""
                    cursor.execute(statement,(session['user'],))
                    line2=cursor.fetchone()
                pack=list(line)
                pack.append(str(session['user']))
                pack.append(line2[0])
                
                for i in messageHolder:
                    print(i[3])
                
                with psycopg2.connect(adress) as conn:
                    cursor=conn.cursor()
                    statement="""SELECT headofclan FROM users WHERE username=%s"""
                    cursor.execute(statement,(session['user'],))
                    line3=cursor.fetchone()
                
                    if line3[0] == True:
                        with psycopg2.connect(adress) as conn:
                            cursor=conn.cursor()
                            statement="""SELECT *FROM request WHERE clan_id=%s"""
                            cursor.execute(statement,(line[6],))
                            line4=cursor.fetchall()
                            
                            if line4:
                                if messageHolder and messageHolder2:
                                    return render_template("user.html",variable=pack,func=clanidtoname,req=line4,funcx=idToUserName,delUser=delUser,message=messageHolder,message2=messageHolder2,la=lastActivities(lineq)) 
                                elif messageHolder2:
                                    return render_template("user.html",variable=pack,func=clanidtoname,req=line4,funcx=idToUserName,delUser=delUser,message2=messageHolder2,la=lastActivities(lineq))
                                elif messageHolder:
                                    return render_template("user.html",variable=pack,func=clanidtoname,req=line4,funcx=idToUserName,delUser=delUser,message=messageHolder,la=lastActivities(line))
                                else:
                                    return render_template("user.html",variable=pack,func=clanidtoname,req=line4,funcx=idToUserName,delUser=delUser,la=lastActivities(lineq))
                if messageHolder and messageHolder2: 
                    return render_template("user.html",variable=pack,func=clanidtoname,funcx=idToUserName,delUser=delUser,message=messageHolder,message2=messageHolder2,la=lastActivities(lineq))
                elif messageHolder2:
                    return render_template("user.html",variable=pack,func=clanidtoname,funcx=idToUserName,delUser=delUser,message=messageHolder2,la=lastActivities(lineq))
                elif messageHolder:
                    return render_template("user.html",variable=pack,func=clanidtoname,funcx=idToUserName,delUser=delUser,message=messageHolder,la=lastActivities(lineq))
                
                else: 
                    return render_template("user.html",variable=pack,func=clanidtoname,funcx=idToUserName,delUser=delUser,la=lastActivities(lineq))
            
        except psycopg2.DatabaseError as e:
            conn.rollback()
            conn.close()
    else:
        return redirect(url_for('login'))

@app.route('/user/<var>/deleteProfile', methods=['GET','POST'])
def deleteProfile(var): ## deletes user
    if 'user' in session:
        DeleteUser(var)
        return redirect(url_for('logout'))
    else:
        return redirect(url_for('login'))
        
@app.route('/user/<var>/editProfile', methods=['GET','POST'])
def editProfile(var): ## edit profile
    if 'user' in session and session['user']==idToUserName(var):
        formU=UserNameEditForm()
        formP=PasswordEditForm() ## different forms cretaed for different attributes. and validation process is done
        formE=EmailEditForm()
        formA=AvatarEditForm()
        with psycopg2.connect(adress) as conn:
            cursor=conn.cursor()
            statement="""SELECT *FROM users WHERE username=%s"""
            cursor.execute(statement,(idToUserName(var),))
            line=cursor.fetchone()
            if formU.validate_on_submit():
                try:
                    statement="""UPDATE users SET username=%s WHERE id=%s"""
                    cursor.execute(statement,(formU.username.data,var))
                    session.pop('user',None)
                    session['user']=formU.username.data
                except psycopg2.DatabaseError as e:
                    if "username" in e.args[0]:
                        conn.rollback()
                        return render_template('editlayout.html',variable=line,formU=formU,formP=formP,formE=formE,formA=formA,errorU="The username is already in use")
    
            if formP.validate_on_submit():
                statement="""SELECT pass_word FROM users WHERE username=%s"""
                cursor.execute(statement,(idToUserName(var),))
                data = cursor.fetchone()
                if data is not None:
                    
                    statement2="""SELECT *FROM users WHERE username=%s"""
                    cursor.execute(statement2,(idToUserName(var),))
                    line=cursor.fetchone()
                
                print(data[0])
                if hasher.verify(str(formP.password3.data),data[0]) is True:
                    try:
                        statement="""UPDATE users SET pass_word=%s WHERE id=%s"""
                        crypt=hasher.hash(formP.password2.data)
                        cursor.execute(statement,(crypt,var))
                        
                    except psycopg2.DatabaseError as e:
                        return render_template('editlayout.html',variable=line,formU=formU,formP=formP,formE=formE,formA=formA)
                else:
                    return render_template('editlayout.html',variable=line,formU=formU,formP=formP,formE=formE,formA=formA,errorP="The password you entered did not match our records. Please double-check and try again.")
            if formE.validate_on_submit():
                try:
                    statement="""UPDATE users SET email=%s WHERE id=%s"""
                    cursor.execute(statement,(formE.email1.data,var))
            
                except psycopg2.DatabaseError as e:
                    if "email" in e.args[0]:
                        conn.rollback()
                        return render_template('editlayout.html',variable=line,formU=formU,formP=formP,formE=formE,formA=formA,errorE="The email address is already in use")
            if formA.validate_on_submit():
                try:
                    os.remove("static/avatars/"+line[3])
                    statement="""UPDATE users SET avatarpath=%s WHERE id=%s"""
                    filename = secure_filename(formA.upload.data.filename)
                    filename = filename+str(datetime.datetime.utcnow())
                    formA.upload.data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    cursor.execute(statement,(filename,var))
                   
                except psycopg2.DatabaseError as e:
                    return render_template('editlayout.html',variable=line,formU=formU,formP=formP,formE=formE,formA=formA)
    else:
        return redirect(url_for('login'))
    return render_template('editlayout.html',variable=line,formU=formU,formP=formP,formE=formE,formA=formA)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081, debug=False)
        