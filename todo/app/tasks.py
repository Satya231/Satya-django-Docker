from todo import settings
from celery import shared_task
from django.core.mail import send_mail
from .models import MyCustomModel,user_otp



@shared_task(bind=True)
def send_email(self,user_id):
    usr = MyCustomModel.objects.get(id = user_id)
    user = user_otp.objects.get(user=usr)

    msg = f'Hii {usr.email} Your otp is {user.otp}'

    send_mail(
        "Welcome to our ToDo App. plz verify your mail",
                 msg,
                 settings.EMAIL_HOST_USER,
                 [usr.email,],
                 fail_silently =True ,
    )
    return "Done"