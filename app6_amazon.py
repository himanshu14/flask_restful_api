#!usr/bin/python
from flask import Flask, jsonify
from werkzeug import generate_password_hash, check_password_hash
from flask import Flask, render_template, json, request
from flask_mysqldb import MySQL
from flask import session,redirect
import time

app = Flask(__name__)
app.secret_key = 'absurd mango and annoying orange'

mysql = MySQL(app) 
# MySQL configurations
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'database'
app.config['MYSQL_HOST'] = 'hostname'
#mysql.init_app(app)


# user login
@app.route('/V1/newLogin',methods=['POST'])
def postUser():
	_email = request.json['inputEmail']
	_password = request.json['inputPassword']
	_hashed_password = generate_password_hash(_password)
	conn = mysql.connection
	cursor = conn.cursor()
	cursor.callproc('sp_createUser',(_email,_hashed_password))
	data = cursor.fetchall()
	if len(data) is 0:
		conn.commit()
	else:
		return json.dumps({'message':'User already exists'})
	cursor.close()
	cursor = conn.cursor()
	cursor.callproc('sp_validateLogin',(_email,))
	data1=cursor.fetchall()
	if check_password_hash(str(data1[0][2]),_password):
		return json.dumps({'message':'User created successfully !','id':data1[0][0]})
	else:
 		return json.dumps({'error':str(data[0])})

# update password
@app.route('/V1/updatePassword',methods=['POST'])
def updatePassword():
	_email = request.json['inputEmail']
	_password = request.json['inputPassword']
	_hashed_password = generate_password_hash(_password)
	conn = mysql.connection
	cursor = conn.cursor()
	cursor.callproc('sp_updateUser',(_email,_hashed_password))
	data = cursor.fetchall()
	if len(data) is 0:
		conn.commit()
		return json.dumps({'message':'Password updated successfully !'})
	else:
 		return json.dumps({'error':str(data[0])})


# user login facebook
@app.route('/V1/newLoginfb',methods=['POST'])
def postUserfb():
	_email = request.json['inputEmail']
	conn = mysql.connection
	cursor = conn.cursor()
	cursor.callproc('sp_createUserfb',(_email,))
	data = cursor.fetchall()
	if len(data) == 0:
		conn.commit()
		cursor.callproc('sp_validateLoginfb',(_email,))
		data1=cursor.fetchall()
		return json.dumps({'message':'User created successfully !','id':data1[0]})
	else:
 		return json.dumps({'message':'User exists','id':str(data[0])})



# check login
@app.route('/V1/validateLogin',methods=['GET'])
def validateLogin():
	_username = request.json['inputEmail']
	_password = request.json['inputPassword']
	_hashed_password = generate_password_hash(_password)
	# connect to mysql
	conn = mysql.connection
	cursor = conn.cursor()
	cursor.callproc('sp_validateLogin',(_username,))
	data = cursor.fetchall()
	if len(data) > 0:
		if check_password_hash(str(data[0][2]),_password):
#			session['user'] = data[0][0]
			return json.dumps({'message':'Logged in','id':data[0][0]})
		else:
			return json.dumps({'error':'Wrong Email address or Password.'})
	else:
		return json.dumps({'error':'Wrong Email address or Password.'})


# check login fb
@app.route('/V1/validateLoginfb',methods=['GET'])
def validateLoginfb():
	_username = request.json['inputEmail']
	_hashed_password = generate_password_hash(_password)
	# connect to mysql
	conn = mysql.connection
	cursor = conn.cursor()
	cursor.callproc('sp_validateLoginfb',(_username,))
	data = cursor.fetchall()
	if len(data) == 0:
		return redirect('/userHome')
	else:
		return json.dumps({'error':''})


# loan details
@app.route('/V1/loanDetails',methods=['POST'])
def loanDetails():
	_id = request.json['id']
	_firstname = request.json['inputFname']
	_lastname = request.json['inputLname']
	_mobilenumber = request.json['inputMnumber']
	_email = request.json['inputEmail']
	_age = request.json['inputAge']
	_gender = request.json['inputGender']
	_city = request.json['inputCity']
	_maritalstatus = request.json['maritalStatus']
	_employmentstatus = request.json['employmentStatus']
	_homeownership = request.json['homeOwnership']
	_monthlysalary = request.json['monthlySalary']
	_monthlyexpend = request.json['monthlyExpend']
	_pan = request.json['PAN']
	_createdus=str(time.strftime("%Y%m%d%H%M%S"))
	# connect to mysql
	conn = mysql.connection
	cursor = conn.cursor()
	cursor.callproc('sp_loanDetails',(_id,_firstname,_lastname,_mobilenumber,_email,_age,_gender,_city,_maritalstatus,_employmentstatus,_homeownership,_monthlysalary,_monthlyexpend,_pan,_createdus))
	conn.commit()
	return 'OK'



# user apps
@app.route('/V1/newApps',methods=['POST'])
def userApps():
	_imei = request.json['imei']
	_mac = request.json['mac_address']
	_details = request.json['details']
	_created = request.json['created_on_timestamp']
	_createdus=str(time.strftime("%Y%m%d%H%M%S"))
	conn = mysql.connection
	cursor = conn.cursor()
	for i in range(len(_details)):
		_package=_details[i]["packageName"]
		_version=_details[i]["versionCode"]
		cursor.callproc('sp_createApps',(_imei,_mac,_package,_created,_version,_createdus))
	conn.commit()
	return 'OK'


# user sms
@app.route('/V1/newSms',methods=['POST'])
def userSms():
	_imei = request.json['imei']
	_mac = request.json['mac_address']
	_details = request.json['details']
	_created = request.json['created_on_timestamp']
	_createdus=str(time.strftime("%Y%m%d%H%M%S"))
	conn = mysql.connection
	cursor = conn.cursor()
	for i in range(len(_details)):
		_body=_details[i]["body"]
		_senderid=_details[i]["sender_id"]
		_messagetimestamp=_details[i]["message_timestamp"]
		cursor.callproc('sp_createSms',(_imei,_mac,_body,_messagetimestamp,_created,_createdus))
	conn.commit()
	return 'OK'




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
