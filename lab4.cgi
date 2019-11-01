#! /usr/bin/python3

import cgi
import MySQLdb
import passwords
import cgitb
import os
import json
cgitb.enable()

form = cgi.FieldStorage()

if "PATH_INFO" in os.environ:
	path_info = os.environ["PATH_INFO"]
else:
	path_info = ""

conn = MySQLdb.connect(host = passwords.SQL_HOST,
user = passwords.SQL_USER,
passwd = passwords.SQL_PASSWD,
db = "clinton")

cursor = conn.cursor()
# send an SQL command to the DB
cursor.execute("SELECT * FROM Area51;")

results = cursor.fetchall()

cursor.close()

def redirect():
	print("Status: 302 Redirect")
	print("Location: lab4.cgi/")
	print()

def redirectedAgain(new):
	print("Status: 302 Redirect")
	print("Location: courses/" + str(new))
	print() 

def getPath(i):
	x = {"id": results[i][0], "area": results[i][1], "raider": results[i][2], "alien": results[i][3],\
		"URL": "cgi-bin/lab4.cgi/courses/" + str(results[i][0])}
	return x

def courses():
	print("Content-Type: application/json")
	print("Status: 200 OK")
	print()

if path_info == "":
	redirect()

elif path_info == "/courses":
	print("Content-Type: application/json")
	print("Status: 200 OK")
	print()
	y = []
	for i in range(0, len(results)):
		x = {"id": results[i][0], "area": results[i][1], "raider": results[i][2], "alien": results[i][3],\
			"URL": "cgi-bin/lab4.cgi/courses/" + str(results[i][0])}
		y.append(x)
		x_json = json.dumps(y, indent=2)
	print(x_json)

elif "add/courses/" in path_info:
	print("Content-Type: application/json")
	print("Status: 200 OK")
	print()
	if (len(path_info) > 13):
		test = []
		test.append(getPath(int(path_info[13:])-3))
		test_json = json.dumps(test, indent=2)
		print(test_json)
	else:
		print("ERROR! Invalid Route!")

elif "/courses/" in path_info:
	print("Content-Type: application/json")
	print("Status: 200 OK")
	print()
	y = []
	for i in range(3, len(results)+3):
		if path_info == "/courses/" + str(i):
			y.append(getPath(i-3))
	y_json = json.dumps(y, indent=2)
	print(y_json)

elif path_info == "/new_form":
	print("Content-Type: text/html")
	print("Status: 200 OK")
	print()
	print("""
	<html>
	<title> Enter a new raider info </title>
	<body>
	<form action="add/" method="POST">
	<p> Area:
		
	<br>
	<input type="number" name="area">
	</p>
	<p> Raider Name:
		
	<br>
	<input type="text" name="raider">
	</p>
	<p> Alien Name:
	<br>
	<input type="text" name="alien">
	<input type = "submit">
	</p>
	</form>
	</body>
	</html>""")

elif path_info == "/add/":
	area = form["area"].value
	raider = form["raider"].value
	alien = form["alien"].value
	ids = len(results)

	cursor = conn.cursor()
	sql = "INSERT INTO Area51 (id, area, RaiderName, AlienName) VALUES (%s, %s, %s, %s)"
	val = (len(results)+3, area, raider, alien)
	cursor.execute(sql, val)
	new_id = cursor.lastrowid
	conn.commit()
	redirectedAgain(new_id)
	cursor.close()

else:
	print("Content-Type: text/html")
	print("Status: 200 OK")
	if path_info != "/":
		print("PATH_INFO: " + path_info)
		print("ERROR: Invalid path")
	print("""
    	<html>
    	<title> default page </title>
    	<body>
    	<h3> Directory </h3>
	<h4><a href="/cgi-bin/lab4.cgi/courses">courses</a></h4>
	<h4><a href="/cgi-bin/lab4.cgi/new_form">insert form</a></h4>
    	</body>
    	</html> """)
	
conn.close()

