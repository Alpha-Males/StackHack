import smtplib, ssl
import re
import socket
import smtplib
import dns.resolver

from flask import flash
from flask_login import current_user
from todo.model import User,Tasks


def label_stat():
    pcount=Tasks.query.filter_by(label='personal',user_id=current_user.id).count()
    wcount=Tasks.query.filter_by(label='work',user_id=current_user.id).count()
    scount=Tasks.query.filter_by(label='shopping',user_id=current_user.id).count()
    ocount=Tasks.query.filter_by(label='other',user_id=current_user.id).count()
    total=pcount+wcount+scount+ocount

    personal=pcount/total
    work=wcount/total
    shopping=scount/total
    other=ocount/total
    return personal,work,shopping,other

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
label = ["personal", "work", "shopping", "other"]
    """
    try:
        user=User.query.filter_by(id=curr_user).first()
        task=Tasks.query.filter_by(user_id=curr_user).all()
        port = 465
        smtp_server = "smtp.gmail.com"
        sender_email = "stackhackforme@gmail.com"
        receiver_email = user.email
        password = 'stackhack@123$'
        personal,work,shopping,other=label_stat()
        data=''
        for i,j in enumerate(task):
            data +='{} '.format(i)+'{}'.format(j.title)+' added by you '+'{}'.format(j.adddate.date())+'\n'
        print(data)
        message = """\
        Subject: Task for the day.
        hi {} hopes you are doing fine
        here are your task for the day.
        your analysis for the week

        Personal {} %
        work {} %
        shopping {} %
        other {} %
        your due tasks
        {}.""".format(user.username,personal*100,work*100,shopping*100,other*100,data)


        context = ssl.create_default_context()

        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)
        return 'sent'
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
