from flask import g,Flask, render_template,redirect,session
from flask import request
from flaskext.mysql import MySQL
import sys
import os
import flask_login
from flask.sessions import SecureCookieSessionInterface
from flask_login import user_loaded_from_header
from passlib.hash import sha256_crypt

app = Flask(__name__)
app.secret_key = os.urandom(24)

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'user'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
    	details = request.form
    	user = details['user']
    	passw= details['pass']
    	conn = mysql.get_db().cursor()
    	conn.execute("""SELECT * FROM user""")
    	record=conn.fetchall()
    	ada = "false"
    	for row in record:
    		if(user == row[0]):
	    		if(sha256_crypt.verify(passw, row[1])):
	    			ada = "true"
	    			session['user'] = user
	    			break;
    	if(ada == "true"):
    		return redirect('/main')
    	else:
    		return render_template('index.html',value='User atau Password salah')
    		 
    	return render_template('index.html')
    return render_template('index.html')

@app.route('/main')
def main():
	return render_template('main.html',user=session['user'])

@app.route('/posts')
def posts():
	return render_template('posts.html')

@app.route('/akun')
def akun():
	return render_template('akun.html')

@app.route('/lupa', methods=['GET', 'POST'])
def lupa():
    if request.method == "POST":
    	details = request.form
    	user = details['user']
    	lupa= details['lupa']
    	conn = mysql.get_db().cursor()
    	conn.execute("""SELECT * FROM user""")
    	record=conn.fetchall()
    	ada = "false"
    	for row in record:
    		if(user == row[0]):
	    		if(sha256_crypt.verify(lupa, row[2])):
	    			ada = "true"
	    			break;
    	if(ada == "true"):
    		return redirect('/')
    	else:
    		return redirect('/lupa')
    return render_template('lupa.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
	if request.method == "POST":
		details = request.form
		user = details['user']
		passw= details['pass']
		Lupa = details['lupa']
		conn = mysql.get_db().cursor()
		if( not user or not passw or not Lupa):
			print("Masukkan semua data",file=sys.stderr)
			conn.close()
			return redirect('/register')
		else:
			conn.execute("INSERT INTO user(username, password, lupa) VALUES (%s, %s, %s)", (user, sha256_crypt.encrypt(passw), sha256_crypt.encrypt(Lupa)))
			mysql.get_db().commit()
			conn.close()
			return redirect('/')
		
	return render_template('register.html')


if __name__ == '__main__':
	app.secret_key = os.urandom(24)
	app.run()