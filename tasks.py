from app import celery,mail,app
from flask_mail import Mail, Message

@celery.task(bind=True)
def send_async_email(self,email_data):
    """Background task to send an email with Flask-Mail."""
    msg = Message(email_data['name'],
                  sender=app.config['MAIL_DEFAULT_SENDER'],
                  recipients=[email_data['to']])
    msg.body = email_data['comment'] 
    with app.app_context():
        try:
            mail.send(msg)
        except Exception as e:
            raise self.retry(exc=e, countdown=60, max_retries=3)

@celery.task(bind=True)
def send_async_wx(self,wx_data):
    get_token=weChat('ww95330520c75e416d','HwJ-Pzl01S7-qVKH8Yq03LQBzwbBmjEDBzPAOgMFcao')
    try:
        get_token.send_message(wx_data['user'],wx_data['content'])
    except Exception as e:
        raise self.retry(exc=e, countdown=60, max_retries=3)

@celery.task(bind=True)
def send_async_sms(self,sms_data):
    try:
        run(sms_data['phone'],sms_data['content'])
    except Exception as e:
        raise self.retry(exc=e, countdown=60, max_retries=3)
