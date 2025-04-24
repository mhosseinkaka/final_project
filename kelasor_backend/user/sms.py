from kavenegar import KavenegarAPI, APIException, HTTPException
from django.conf import settings

def send_otp_sms(phone, code):
    try:
        api = KavenegarAPI('484C7571326A3573413549737736714853344858424A39364F6A4B5A724F70594C38396C6F5755517262593D')
        params = {
            'receptor': phone,
            'template': settings.KAVENEGAR_TEMPLATE,
            'token': code,
            'type': 'sms'  # یا call
        }
        api.verify_lookup(params)
    except APIException as e:
        print("Kavenegar API Error:", e)
    except HTTPException as e:
        print("HTTP Error:", e)