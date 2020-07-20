from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)


app.secret_key = '123456'



app.config['MYSQL_HOST'] = 'pythonapi2020.mysql.pythonanywhere-services.com'
app.config['MYSQL_USER'] = 'pythonapi2020'
app.config['MYSQL_PASSWORD'] = 'data6473969903'
app.config['MYSQL_DB'] = 'pythonapi2020$data'


mysql = MySQL(app)
mesg = ''

#  Login USer Code 
# =================================================================
@app.route('/', methods=['GET', 'POST'])
def login():
    msg = ''
    email = ''
    if request.method == 'POST' and 'userName' in request.form and 'userPass' in request.form:

        userName = request.form['userName']
        userPass = request.form['userPass']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user_management WHERE userName = %s AND userPass = %s', (userName, userPass,))

        account = cursor.fetchone()

        if account:
            session['loggedin'] = True
            session['id'] = account['ID']
            session['username'] = account['userName']
            session['userpass'] = account['userPass']
            session['useremail'] = account['userEmail']
            return render_template('home.html', msg=session['username'])
        else:
            msg = 'Incorrect username/password!'
    return render_template('index.html', msg=msg)

    

@app.route('/pylog/admin', methods=['GET', 'POST'])
def admin():
    msg = ''

    if request.method == 'POST' and 'userName' in request.form and 'userPass' in request.form:

        userName = request.form['userName']
        userPass = request.form['userPass']
                
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM admin WHERE adminName = %s AND adminPass = %s', (userName, userPass,))
        
        account = cursor.fetchone()
                
        if account:
            msg = 'Welcome back! ' + userName
            return render_template('admin_home.html', msg=msg)
        else:
            
            msg = 'Incorrect username/password!'
    return render_template('adminlog.html', msg=msg)

    # Logout Code 
    #================================================================

@app.route('/pylog/logout')
def logout():

   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   return redirect(url_for('login'))

   # Register Code 
   #===================================================================
@app.route('/pylog/register', methods=['GET', 'POST'])
def register():

    msg = ''
    
    if request.method == 'POST' and 'userName' in request.form and 'userPass' in request.form and 'userEmail' in request.form and 'fName' in request.form and 'lName' in request.form and 'prof' in request.form and 'states' in request.form and 'lastlogin' in request.form:

        userName = request.form['userName']
        userPass = request.form['userPass']
        userEmail = request.form['userEmail']
        fName = request.form['fName']
        lName = request.form['lName']
        prof = request.form['prof']
        gender = request.form['gender']
        states = request.form['states']
        lastlogin = request.form['lastlogin']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user_management WHERE userName = %s OR userEmail = %s' , (userName, userEmail,))
        account = cursor.fetchone()

        if account:
            msg = 'User Name or Email already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', userEmail):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', userName):
            msg = 'Username must contain only characters and numbers!'
        elif not userName or not userPass or not userEmail:
            msg = 'Please fill out the form!'
        else:
            cursor.execute('INSERT INTO user_management VALUES (NULL, %s, %s, %s)', (userName, userPass, userEmail,))
            mysql.connection.commit()
            cursor.execute('SELECT * FROM user_management ORDER BY ID desc')
            uID = cursor.fetchone()
            lastID = uID['ID']
            cursor.execute('INSERT INTO `users` VALUES (%s, %s, %s, %s, %s, %s, %s)', (lastID, fName, lName, prof, gender, states, lastlogin,))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':

        msg = 'Please fill all required information!'

    return render_template('register.html', msg=msg)


    #=====================================================================
@app.route('/pylog/home')
def home():

    if 'loggedin' in session:

        return render_template('home.html', msg=session['username'])

    return redirect(url_for('login'))

    # Profile Code 
    #====================================================================
@app.route('/pylog/user_profile')
def user_profile():

    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user_management WHERE ID = %s', (session['id'],))
        account = cursor.fetchone()

        cursor.execute('SELECT * FROM `users` WHERE ID = %s', (session['id'],))
        user = cursor.fetchone()

        return render_template('profile.html', account=account, user=user)
    return redirect(url_for('login'))

    # Edit Profile Code 
    #=========================================================
@app.route('/pylog/changedata', methods=['GET', 'POST'])
def changedata():

    msg = ''

    if request.method == 'POST' and 'userName' in request.form and 'userPass' in request.form and 'userEmail' in request.form and 'fName' in request.form and 'lName' in request.form and 'prof' in request.form and 'states' in request.form and 'lastlogin' in request.form:

        userName = request.form['userName']
        userPass = request.form['userPass']
        userEmail = request.form['userEmail']
        fName = request.form['fName']
        lName = request.form['lName']
        prof = request.form['prof']
        gender = request.form['gender']
        states = request.form['states']
        lastlogin = request.form['lastlogin']
        userID = session['id'];

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user_management WHERE (userName = %s OR userEmail = %s) AND ID <> %s' , (userName, userEmail,userID,))
        account = cursor.fetchone()

        if account:
            msg = 'User Name or Email already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', userEmail):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', userName):
            msg = 'Username must contain only characters and numbers!'
        elif not userName or not userPass or not userEmail:
            msg = 'Please fill out the form!'
        else:

            cursor.execute('UPDATE user_management set userName = %s, userPass = %s, userEmail = %s WHERE ID = %s' , (userName, userPass, userEmail, userID,))
            mysql.connection.commit()
            cursor.execute('UPDATE users set first_name = %s, last_name = %s, profession = %s, gender = %s, states = %s, last_login = %s WHERE ID = %s' , (fName, lName, prof, gender, states, lastlogin, userID,))
            mysql.connection.commit()
            msg = 'You have successfully change profile!'
            cursor.execute('SELECT * FROM user_management WHERE  ID = %s' , (userID,))
            account = cursor.fetchone()
            cursor.execute('SELECT * FROM `users` WHERE ID = %s', (userID,))
            user = cursor.fetchone()
            return render_template('profile.html', account=account, user=user, msg=msg)
    elif request.method == 'POST':

        msg = 'Please fill all required information!'

    return render_template('profile.html', account=account, user=user, msg=msg)

      # Forget Password Code 
    #=========================================================
@app.route('/pylog/forgetpass', methods=['GET', 'POST'])
def forgetpass():

    msg = ''

    if request.method == 'POST' and 'userName' in request.form and 'userEmail' in request.form:

        userName = request.form['userName']
        userEmail = request.form['userEmail']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user_management WHERE userName = %s AND userEmail = %s', (userName, userEmail,))

        account = cursor.fetchone()

        if account:
            user = userName
            return render_template('resetpass.html', msg=msg, user=user)
        else:

            msg = 'Username or Email not found!'
    return render_template('forgetpass.html', msg=msg)


    #=========================================================
@app.route('/pylog/reset_pass', methods=['GET', 'POST'])
def reset_pass():

    msg = ''

    if request.method == 'POST' and 'userName' in request.form and 'userPass' in request.form and 'userPass2' in request.form:

        userName = request.form['userName']
        userPass = request.form['userPass']
        userPass2 = request.form['userPass2']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user_management WHERE userName = %s' , (userName,))
        account = cursor.fetchone()
        if not userPass or not userPass2:
            msg = 'Please fill out the form!'
        elif userPass != userPass2:
            msg = 'Password mismatch!'
        else:
            cursor.execute('UPDATE user_management set userPass = %s WHERE userName = %s' , (userPass, userName,))
            mysql.connection.commit()
            msg = 'You have successfully reset password!'
            return render_template('index.html')
    elif request.method == 'POST':

        msg = 'Please fill all required information!'

    return render_template('resetpass.html', msg=msg, user=userName)