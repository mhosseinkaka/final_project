from kelasor_backend.celery import shared_task
from user.sms import send_otp_sms

@shared_task
def send_otp_task(phone, code):
    send_otp_sms(phone, code)