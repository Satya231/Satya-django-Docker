from django.contrib.auth.signals import user_logged_in, user_logged_out,user_login_failed
from  app.models import MyCustomModel, TODO
from django.dispatch import receiver
from django.db.models.signals import pre_init,post_init,pre_save,post_init,post_save,pre_delete,post_delete
from django.core.cache import cache


@receiver(user_logged_in, sender =MyCustomModel)
def login_successfully(sender,request,user,**kwargs):

    ct = cache.get('count', 0, version=user.pk)
    newcount = ct+1
    cache.set('count', newcount, 60*60*24, version=user.pk)
    print(user.pk)

    print("-------------")
    print("Logged in signal....Run Intro")
    print("Sender: ", sender)
    print("Request: ", request)
    ip = request.META.get('REMOTE_ADDR')
    print("Client IP:", ip)
    request.session['ip'] = ip
    print("User: ", user)
    print("User Password: ", user.password)
    print(f'kwargs: {kwargs}')
#user_logged_in.connect(login_successfully, sender=MyCustomModel)




@receiver(user_logged_out, sender =MyCustomModel)
def log_out(sender,request,user,**kwargs):
    print("-------------")
    print("Logged out signal....Run Outro")
    print("Sender: ", sender)
    print("Request: ", request)
    print("User: ", user)
  
    print(f'kwargs: {kwargs}')
#user_logged_out.connect(log_out, sender=MyCustomModel)

@receiver(user_login_failed)
def login_failed(sender,credentials, request,**kwargs):
    print("-------------")
    print("Login failed signal....Run Outro")
    print("Sender: ", sender)
    print("Credentials: ", credentials)
  
    print(f'kwargs: {kwargs}')

@receiver(pre_save,sender= TODO)
def at_beginning_save(sender,instance,**kwargs):
    print("-------------")
    print("Pre save signal....Run Outro")
    print("Sender: ", sender)
    print("Instance: ", instance)
  
    print(f'kwargs: {kwargs}')
#pre_save.connect(at_beginning_save, sender=POST)

@receiver(post_save,sender= TODO)
def at_ending_save(sender,instance,created,**kwargs):
    if created:
        print("-------------")
        print("New Record",)
        print("Post save signal....Run Outro")
        print("Sender: ", sender)
        print("Instance: ", instance)
        print("Created:: ", created)
        print(f'kwargs: {kwargs}')
    else:
        print("-------------")
        print("Update ",)
        print("Post save signal....Run Outro")
        print("Sender: ", sender)
        print("Instance: ", instance)
        print("Created:: ", created)
        print(f'kwargs: {kwargs}')

#post_save.connect(at_ending_save, sender=POST)
