from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from django.utils import timezone






# Create your models here
# .
class MyCustomModelManager(BaseUserManager):

    def create_user(self,  email,  password=None):
       
        if not email:
            raise ValueError("Users must have an email address")
        # if not username:
        #      raise ValueError("Users must have a username")
        
        user  = self.model(
            
            email = self.normalize_email(email), #normalize-doesn't care about case sensitivity
            #username = username
        )
        user.set_password(password)
        user.save()   #(using = self._db)--used when multiple databases are there
        return user

    def create_superuser(self,  email,  password,**extra_fields):
        user = self.create_user(
            
            email = self.normalize_email(email),
            #username = username,
            password = password, 
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save()       #(using = self._db)
        return user
        



        


class MyCustomModel(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(verbose_name="Email",unique=True, max_length=60,  null=True)
    username = None
    date_joined = models.DateTimeField(default=timezone.now)
    is_admin = models.BooleanField(default = False)
    is_active = models.BooleanField(default = True)
    is_staff = models.BooleanField(default = False)
    is_superuser = models.BooleanField(default = False)

    
    

    objects = MyCustomModelManager()


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


    # def __str__(self):
    #     return self.username

    # def has_perm(self, perm, obj=None):
    #     return self.is_admin

    # def has_module_perms(self, app_label):
    #     return True








class TODO(models.Model):
    status_choices = [
    ('C', 'COMPLETED'),
    ('P', 'PENDING'),
    ]
    priority_choices = [
    ('1', '1️⃣'),
    ('2', '2️⃣'),
    ('3', '3️⃣'),
    ('4', '4️⃣'),
    ('5', '5️⃣'),
    ('6', '6️⃣'),
    ('7', '7️⃣'),
    ('8', '8️⃣'),
    ('9', '9️⃣'),
    ('10','🔟'),
    ]
    tasks = models.CharField(max_length=50)
    status = models.CharField(max_length=10 , choices=status_choices)
    user = models.ForeignKey(MyCustomModel, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    priority = models.CharField(max_length=2 , choices=priority_choices)
    image = models.FileField(upload_to = 'picture' ,max_length = 255,null=True)
    text = models.TextField(blank=True, null=True )
     #pip install pillow for images

    def __str__(self):
        return self.tasks

    # def save(self, *args, **kwargs):
    #     try:
    #         this = TODO.objects.get(id=self.id)
    #         if this.image:
    #             this.image.delete()   
    #     except ObjectDoesNotExist: 
    #         pass        
    #     super(TODO, self).save(*args, **kwargs)

    

class user_otp(models.Model):
    user = models.OneToOneField(MyCustomModel, on_delete=models.CASCADE, null=True, blank=True)
    otp =  models.SmallIntegerField()

    def __str__(self):
        return str(self.user)


# class Chat(models.Model):
#     content = models.CharField(max_length=1000)
#     timestamp = models.DateTimeField(auto_now=True)
#     group = models.ForeignKey('Group', on_delete=models.CASCADE)

# class Group(models.Model):
#     name = models.CharField(max_length = 255)

#     def __str__(self):
#         return self.name 


    

    


#custom user model

#create a new user
#cfreate a superuser

