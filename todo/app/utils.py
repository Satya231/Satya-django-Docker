from django.conf import settings
from django.core.mail import send_mail
from .models import MyCustomModel,user_otp


def send_email(user_id):
    usr = MyCustomModel.objects.get(user = user_id)
    msg = f'Hii {usr.username} Your otp is {user_otp.otp}'

    return send_mail(
        "Welcome to our ToDo App. plz verify your mail",
                 msg,
                 settings.EMAIL_HOST_USER,
                 [usr.email,],
                 fail_silently = False,
    )
    #return send_mail()