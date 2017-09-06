'''
If you want to enable email service, set the email address in secret.py and uncomment the code related to sender.
'''
from cStringIO import StringIO
from imaplib import IMAP4_SSL
from platform import python_version
from poplib import POP3_SSL
from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import secret 
import time
import threading
import sys
sys.path.append('..')
from app import get_email


    

class sender(threading.Thread):

	def __init__(self,imgName,warningType):
		self.imgName = imgName
	        self.warningType = warningType
	        threading.Thread.__init__(self)

	def run(self):
                print 'sending'
		time.sleep(4)
		self.send(self.imgName,self.warningType)

	def send(self,imgName,warningType):
		info = secret.getInfo()
		MAILBOX = info['MAILBOX']
		PASSWD = info['PASSWD']

		release = python_version
		if release >'2.6.2':
			from smtplib import SMTP_SSL
		else:
			SMTP_SSL = None



		who = '%s@gmail.com' %MAILBOX
		from_ = who
		to = ','.join(get_email.get_email_addr())

		COMMASPACE = ', '

		# Create the container (outer) email message.
		msg = MIMEMultipart()
		msg['Subject'] = 'Warning from Intel Edison!!~~'
		# me == the sender's email address
		# family = the list of all recipients' email addresses
		msg['From'] = from_
		msg['To'] = to
		msg.preamble = 'Warning from Intel Edison!!~~'

		timeSlot = "It happened at "+time.strftime('%Y-%m-%d-%H-%M',time.localtime(time.time()))+warningType
		currentTime = MIMEText(timeSlot,'plain')

		html = """\
		<html>
		  <head></head>
		  <body>
		    <p>Some thing Strange!<br>
		       <a href="https://www.python.org">Click here to view the live stream</a>
		    </p>
		  </body>
		</html>
		"""

		htmlPart = MIMEText(html,'html')

                if imgName!='None':
                   fp = open(imgName, 'r')
                   img = MIMEImage(fp.read())
                   fp.close()
                   msg.attach(img)

                msg.attach(currentTime)
		msg.attach(htmlPart)

                s = SMTP('smtp.gmail.com',587)
                if release<'2.6':
                 s.ehlo()
                 s.starttls()
                 s.login(MAILBOX,PASSWD)
                 s.sendmail(from_,to,msg.as_string())
                 s.quit()


	
		
















