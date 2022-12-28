from todo import settings
from celery import shared_task
from django.core.mail import send_mail
from celery.contrib import rdb
from django.http.response import JsonResponse
from celery.utils.log import get_task_logger
from PIL import Image
#import os.path
from pytesseract import pytesseract
import os
from django.core.exceptions import ValidationError
import ipdb
import json






logger = get_task_logger(__name__)


@shared_task
def send_email(usr,otp):
    logger.info("task started")
    #rdb.set_trace()
    
    # usr = MyCustomModel.objects.get(id = user_id)
    #user = user_otp.objects.get(id=user_id)
    
    msg = f'Hello  Welcome To My Todo App. Your otp is {otp}'
   

    send_mail(
        "Welcome to our ToDo App. plz verify your mail",
        msg,
        settings.EMAIL_HOST_USER,
        [usr],
        fail_silently =True ,
        )
    logger.info("task ended")
    
    return  {'status' : True}



# Auto prepending task names to your log output
# The ability to set log handling rules at a higher level than just module (I believe it's actually setting the logger name to celery.task)
# Probably, most importantly for Sentry setup, is it hooks the logging into their log handlers which Sentry makes use of.




@shared_task
def file_validation(image):
    logger.info("task started")
    
    file,ext = os.path.splitext(image)  #python inbuilt function:- To extract an extension of a file name(ext = os.path.splitext(file)) gives tuple-> (file_name,file_ext)
    logger.info("get file name and extension")
    valid_extensions = ['.png','jpg','webp','gif']
    if  ext not in valid_extensions:
        raise ValidationError('Unsupported file type. Only Pdf files are allowed.')
    logger.info("task ended")
    #ipdb.set_trace()
    #image_path = file+ext
    # payload = {'img_file':'image_path'}
    # file = json.dumps(payload)
    return image

@shared_task
def extract_text(image):
    logger.info("task started")
    path_to_tesseract = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    #rdb.set_trace()
    print(img_file)
    img = Image.open(image.img.path, mode='r')
    # print(img)
    pytesseract.tesseract_cmd = path_to_tesseract

    text = pytesseract.image_to_string(img_file)
    logger.info("text extracted")
    return text 