import smtplib

#def prompt (prompt):
#   return input(prompt).strip()

fromaddr    = 'ya@work.com'#prompt("From: ")
toaddrs     = ['doublegee@mail.ru']#prompt("To: " ).split()
#print("Enter message, end with ^Z in win: ")

msg = ("From: %s\r\nTo: %s\r\n\r\n" %(fromaddr, ", ".join(toaddrs)))

#line = input()

#msg = msg + line

msg = 'Subject: Shaverma\r\n'
'Content-type: text/plain; charset=ISO-8859-1\r\n\r\n'
'This is a message body\r\n.\r\n\r\n\r\n'
print ("Message length is", len(msg) )

#options = ['\r\nContent-type: text/plain; charset=ISO-8859-1']

server = smtplib.SMTP('localhost',1025)
server.set_debuglevel(1)
server.sendmail(fromaddr, toaddrs, msg )#, [], options)
server.quit()

