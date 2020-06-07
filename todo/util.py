import smtplib, ssl
import re
import socket
import smtplib
import dns.resolver

from flask import flash

from todo.model import User,Tasks

def verify_email(email):
    """

    """
    records = dns.resolver.query('emailhippo.com', 'MX')
    mxRecord = records[0].exchange
    mxRecord = str(mxRecord)

    # Get local server hostname
    host = socket.gethostname()

    # SMTP lib setup (use debug level for full output)
    server = smtplib.SMTP()
    server.set_debuglevel(0)

    # SMTP Conversation
    server.connect(mxRecord)
    server.helo(host)
    server.mail('smtp@gmail.com')
    code, message = server.rcpt(email)
    server.quit()

    return code

def send_email(curr_user):
    """

    """
    try:
        user=User.query.filter_by(id=curr_user).first()
        task=Tasks.query.filter_by(user_id=curr_user).all()
        port = 465
        smtp_server = "smtp.gmail.com"
        sender_email = "stackhackforme@gmail.com"
        receiver_email = user.email
        password = 'stackhack@123$'

        task_info=[]
        for i in task:
            task_info.append(i.title)
        message = """\
        Subject: Task for the day.

        hi {} hopes you are doing fine
        here are your task for the day.
        Tasks {}.""".format(user.username,task_info)

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)
    except:
        flash(u"this email is invalid","error")

def checkavl(email, username):
    """

    """
    user = User.query.filter_by(username=username).first()
    if user:
        return "username is used before choose something unique"
    user = User.query.filter_by(email=email).first()
    if user:
        return "Seems like you already have an account with this account please login"
    return "Everything fine"
