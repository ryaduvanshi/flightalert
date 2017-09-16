#!/usr/bin/env python
import cgi
import cgitb
cgitb.enable()

import urllib
import MySQLdb

print "Content-type: text/html\n"

page = urllib.urlopen("templates/index.html").read()
print page


db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                     user="root",         # your username
                     passwd="root",  # your password
                     db="roncorpfa")
cur = db.cursor()

#check for data
form = cgi.FieldStorage()
formemail = form.getvalue('email')
formorigin = form.getvalue('origin')
formdest = form.getvalue('dest')
formdate = form.getvalue('date') 
if formemail and formorigin and formdest and formdate:
	add_query = "insert into flrequests (userid, origin, dest, date) values ('"+formemail+"', '"+formorigin+"', '"+formdest+"', "+formdate+");"
	cur.execute(add_query)
	db.commit()

#display added cron
print '<div class="container-fluid col-md-8" >'
print '<h3>Requests list</h3>'
print '<table class="table table-hover"><tr><th>email<th>origin<th>dest<th>date<th>fare<th>flight<th></tr>'

cur.execute("SELECT * FROM flrequests")
for row in cur.fetchall():
	print '<tr><td>' + row[1]
	print '<td>' + row[2]
	print '<td>' + row[3]
	print '<td>' + row[4]
	print '<td>' + str(row[5])
	print '<td>' + row[7]
	print '<td><a class="label label-danger" href = "delete.py?id='+str(row[0])+'">delete</a></tr>';

print '</table></div>'
db.close()	
