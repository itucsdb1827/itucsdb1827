from flask import Flask,render_template,redirect,url_for,session
from flask_wtf import FlaskForm,RecaptchaField
from wtforms import StringField, PasswordField,BooleanField,validators
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug import secure_filename
from wtforms.fields.html5 import EmailField 
import psycopg2
import datetime
from passlib.hash import pbkdf2_sha256 as hasher
import os
import sys

app = Flask(__name__)

##adress="postgres://postgres:159753456@localhost:5432/postgres"
adress="postgres://uyxegmizzcfgoj:3107cb2c0cfd9de6528ff9b966cd87d5040ec3dea13d85c863244efae597e6cb@ec2-54-225-241-25.compute-1.amazonaws.com:5432/d5uaci1fn1qp6d"

UPLOAD_FOLDER='static/avatars/'


    
    


app.config['SECRET_KEY']='ASD159sDGDAFHAFSghsrjrjeacaethehg21f65a1f65e153a1ae5v1a6e5v165gASD'
app.config['RECAPTCHA_PUBLIC_KEY']='6Ldz2nUUAAAAAAOxPyirz5W4T-o0IT-8Z1X9PMcZ'
app.config['RECAPTCHA_PRIVATE_KEY']='6Ldz2nUUAAAAAONNFYvLuTtrZOGNSKT90wHsiN0q'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

noUsernamePasswordFound='The username and password you entered did not match our records. Please double-check and try again.'


class SignUpForm(FlaskForm):
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
    
class LoginForm(FlaskForm):
    username=StringField('Username:',validators=[validators.InputRequired()])
    password=PasswordField('Password:',validators=[validators.DataRequired()])
    

class UserNameEditForm(FlaskForm):
    username=StringField('Username:',validators=[validators.InputRequired(),validators.Length(min=6,max=16,message="Username must be between 6 and 16 characters.")])

class PasswordEditForm(FlaskForm):
    password3=PasswordField('Old Password:',validators=[validators.DataRequired()])
    password1=PasswordField('New Password:',validators=[validators.DataRequired(),validators.Length(min=6,max=16,message="Password must be between 6 and 16 characters."),validators.EqualTo('password2',message="passwords must be equal.")])
    password2=PasswordField('New Password Again:',validators=[validators.DataRequired()])

class EmailEditForm(FlaskForm):
    email1=EmailField('E-mail:',validators=[validators.InputRequired()])

class AvatarEditForm(FlaskForm):
    upload = FileField('Avatar', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png'], 'Images only!')
    ])
    
@app.route('/',methods=['GET']) 
def home():
    return redirect(url_for('login'))

@app.route("/terms",methods=['GET'])
def terms():
    return render_template('terms.html')

@app.route("/faq",methods=['GET'])
def faq():
    return render_template('faq.html')
@app.route("/signup",methods=['GET','POST'])
def signup():
    if 'user' in session:
        return redirect(url_for('user',var=UserNameToId(session['user'])))
    

    print(os.path.join(app.config['UPLOAD_FOLDER']),file=sys.stderr)
    sys.stderr.flush()
    form = SignUpForm()
    if form.validate_on_submit():
        print('no')
        crypt=hasher.hash(form.password1.data)
        try:
            conn=psycopg2.connect(adress)
            f = form.upload.data
            filename = secure_filename(f.filename)
            print(filename)
            filename = filename+str(datetime.datetime.utcnow())
            print(filename)
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
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
                return render_template('home.html', form=form,errorU="The username  is already in use")
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

@app.route("/login",methods=['GET','POST'])
def login():
    if 'user' in session:
        return redirect(url_for('user',var=UserNameToId(session['user'])))
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
                if hasher.verify(str(form.password.data),data[0]) is True:
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
def logout():
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

    
@app.route('/user/<var>', methods=['GET','POST'])
def user(var):
    print(type(var))
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
                pack=list(line)
                pack.append(str(session['user']))
                return render_template("user.html",variable=pack)
            
        except psycopg2.DatabaseError as e:
            conn.rollback()
            conn.close()
    else:
        return redirect(url_for('login'))
def idToUserName(id):
    with psycopg2.connect(adress) as conn:
        cursor=conn.cursor()
        statement="""SELECT *FROM users WHERE id=%s"""
        cursor.execute(statement,(id,))
        line=cursor.fetchone()
        return str(line[1])
        
def UserNameToId(username):  
    with psycopg2.connect(adress) as conn:
        cursor=conn.cursor()
        statement="""SELECT *FROM users WHERE username=%s"""
        cursor.execute(statement,(username,))
        line=cursor.fetchone()
        return str(line[0]) 
      
@app.route('/user/<var>/editProfile', methods=['GET','POST'])
def editProfile(var):
    if 'user' in session and session['user']==idToUserName(var):
        formU=UserNameEditForm()
        formP=PasswordEditForm()
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
    app.run(host="0.0.0.0", port=8082, debug=False)
        