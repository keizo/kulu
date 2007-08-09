# Use this for e-mailing.
# Modified from Django .95 :) TODO: Are there licencing issues with that?

from email.MIMEText import MIMEText
from email.Header import Header
import smtplib
import rfc822
import os

import web

settings = web.storage({})

# Usually leave True, but if you get a socket.error connection refused
# try change it to False.  I use False only for development on localhost
settings.USE_SMTPLIB = False
settings.SENDMAIL_LOCATION = '/usr/lib/sendmail'  # Only used if not using smtplib

# TODO: Should these constants go in glbl.constants? or is that a security 
# issue -- because the password would be store as plain text in the db

settings.EMAIL_HOST = 'ocpaddler.com'
settings.EMAIL_HOST_USER = 'keizo'
settings.EMAIL_HOST_PASSWORD = 'ocp49876d'
settings.EMAIL_PORT = 25
settings.DEFAULT_FROM_EMAIL = 'keizo@ocpaddler.com'
settings.EMAIL_SUBJECT_PREFIX = ''
settings.SERVER_EMAIL = 'root@localhost'
settings.DEFAULT_CHARSET = 'utf-8'

settings.ADMINS = 'keizo@ocpaddler.com'
settings.MANAGERS = 'keizo@ocpaddler.com'

class BadHeaderError(ValueError):
    pass

class SafeMIMEText(MIMEText):
    def __setitem__(self, name, val):
        "Forbids multi-line headers, to prevent header injection."
        if '\n' in val or '\r' in val:
            raise BadHeaderError, "Header values can't contain newlines (got %r for header %r)" % (val, name)
        if name == "Subject":
            val = Header(val, settings.DEFAULT_CHARSET)
        MIMEText.__setitem__(self, name, val)

def send(to, subject, message, from_email, fail_silently=False, 
         auth_user=settings.EMAIL_HOST_USER, 
         auth_password=settings.EMAIL_HOST_PASSWORD):
    """
    Easy wrapper for sending a single message to a recipient list. All members
    of the recipient list will see the other recipients in the 'To' field.
    """
    # Probably shouldn't have to type check, but can't think of a better way..
    if type(to) != type([]):  #then it's probably a single email
        to = [to]
    return send_mass_mail([[subject, message, from_email, to]], fail_silently, auth_user, auth_password)

def send_mass_mail(datatuple, fail_silently=False, auth_user=settings.EMAIL_HOST_USER, auth_password=settings.EMAIL_HOST_PASSWORD):
    """
    Given a datatuple of (subject, message, from_email, recipient_list), sends
    each message to each recipient list. Returns the number of e-mails sent.

    If from_email is None, the DEFAULT_FROM_EMAIL setting is used.
    If auth_user and auth_password are set, they're used to log in.
    """
    try:
        if settings.USE_SMTPLIB:
            server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
            if auth_user and auth_password:
                server.login(auth_user, auth_password)
        else:
            sendmail = os.popen("%s -t" % settings.SENDMAIL_LOCATION, "w")
    except:
        if fail_silently:
            return
        raise
    num_sent = 0
    for subject, message, from_email, recipient_list in datatuple:
        if not recipient_list:
            continue
        from_email = from_email or settings.DEFAULT_FROM_EMAIL
        msg = SafeMIMEText(message, 'plain', settings.DEFAULT_CHARSET)
        msg['Subject'] = subject
        msg['From'] = from_email
        msg['To'] = ', '.join(recipient_list)
        msg['Date'] = rfc822.formatdate()
        try:
            if settings.USE_SMTPLIB:
                server.sendmail(from_email, recipient_list, msg.as_string())
            else:
                sendmail.write(msg.as_string())
            num_sent += 1
        except:
            if not fail_silently:
                raise
    try:
        if settings.USE_SMTPLIB:
            server.quit()
        else:
            sendmail.close()
    except:
        if fail_silently:
            return
        raise
    return num_sent

def mail_admins(subject, message, fail_silently=False):
    "Sends a message to the admins, as defined by the ADMINS setting."
    send_mail(settings.EMAIL_SUBJECT_PREFIX + subject, message, settings.SERVER_EMAIL, [a[1] for a in settings.ADMINS], fail_silently)

def mail_managers(subject, message, fail_silently=False):
    "Sends a message to the managers, as defined by the MANAGERS setting."
    send_mail(settings.EMAIL_SUBJECT_PREFIX + subject, message, settings.SERVER_EMAIL, [a[1] for a in settings.MANAGERS], fail_silently)
