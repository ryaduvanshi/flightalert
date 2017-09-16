#!/usr/bin/env python
import cgi
import cgitb
cgitb.enable()

import MySQLdb

#print "Content-type: text/html\n"

db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                     user="root",         # your username
                     passwd="root",  # your password
                     db="roncorpfa")
cur = db.cursor()

#check for data
form = cgi.FieldStorage()
id1 = form.getvalue('id')
if id1:
	del_query = "delete from flrequests where id = " + id1 ;
	cur.execute(del_query)
	db.commit()

db.close()
#print 'Status: 303 See other'
print 'Location: \ \n'
