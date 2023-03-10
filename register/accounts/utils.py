from django.core.mail import send_mail
from django.conf import settings

def send_otp_code(email , code):
     send_mail('پای ماژول', f'کد ثبت نام شما {code}',settings.EMAIL_HOST_USER,[email,],fail_silently=False)