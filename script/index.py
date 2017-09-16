#!/usr/bin/python

# Turn on debug mode.
import requests
import json
import MySQLdb
import time
import smtplib
from smtplib import SMTPException
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

sender = 'flightalert@roncorp.com'
#sender = 'ubuntu@ip-172-31-27-91.ap-south-1.compute.internal'
#sender = ''

db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                     user="root",         # your username
                     passwd="root",  # your password
                     db="roncorpfa")

cur = db.cursor()

count = 0

while True : 
	cur.execute("SELECT * FROM flrequests")
	for row in cur.fetchall():

		#added for goibibo constraints
		count = count + 1;
		if(count%30 == 0) :
			time.sleep(60) 
			count = 0	
		try:
			r = requests.get('https://developer.goibibo.com/api/stats/minfare/?app_id=cea59fa6&app_key=69ad5273737e4983a6d6428771222354&format=json&vertical=flight&source=' 
				+ row[2]
				+ '&destination='
				+ row[3]
				+'&mode=all&sdate='
				+ row[4]
				+'&class=E');

			data = json.loads(r.text);
			minfare = int(row[5]);
			if minfare == 0 :
				minfare = 10000000;
			flightid = '';

			for key, value in data.items():
				if(value['fare'] != minfare):
					minfare = value['fare'];
					flightid = value['carrier'];
		
			if ( int(row[5]) != minfare ) :
				#send notifications
				receivers = [ row[1] ]
				msg = MIMEMultipart()
				msg['Subject'] = row[2] + " to " + row[3] + " | "+row[4]+" |  changed from Rs. " + str(row[5]) + " to  Rs. " + str(minfare)
				body = "visit http://52.66.99.17 for more"
	#			message = 'Subject:' + row[2] + " to " + row[3] + " | "+row[4]+" |  changed from Rs. " + str(row[5]) + " to  Rs. " + str(minfare) +"<br>\n Body: visit http://52.66.99.17 for more"
				msg.attach(MIMEText(body, 'plain'))
				text = msg.as_string()
				try:
					smtpObj = smtplib.SMTP('localhost')
					smtpObj.sendmail(sender, receivers, text)
					server.quit() 
				except Exception:
					print "Error: unable to send email"
				
				cur.execute("update flrequests set fare = "
					+ str(minfare)
					+ " , flightid =  '"
					+ flightid 
					+ "' where id = "
					+ str(row[0]) + ";");
		except Exception:
			print "error: mostly due to empty json"
	db.commit()
	time.sleep(60)

db.close()
