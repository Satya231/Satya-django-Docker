from django.contrib import admin
from app.models import TODO,MyCustomModel,user_otp
from django.contrib.auth.admin import UserAdmin
from .forms import signupForm

# Register your models here.
class user_otpAdmin(admin.ModelAdmin):
      model = user_otp
      list_display = ('user','otp',)


class TodoAdmin(admin.ModelAdmin):
    model = TODO
    list_display = ('user', 'priority', 'tasks', 'status','image','text')

    ordering =('id',)


class CustomUserAdmin(admin.ModelAdmin):
    
  
    model = MyCustomModel
    list_display = ('id','email', 'date_joined', 'is_staff', 'is_active',)
    add_fieldsets = {
        
        'fields': ('email',  'password1', 'password2'),
    }
    

   
    
    ordering = ('id',)


# class ChatModelAdmin(admin.ModelAdmin):
#     list_display = ['id', 'content', 'timestamp', 'group']

# class GroupModelAdmin(admin.ModelAdmin):
#     list_display = ['id', 'name']



admin.site.register(TODO, TodoAdmin)
admin.site.register(MyCustomModel,CustomUserAdmin)
admin.site.register(user_otp,user_otpAdmin)
# admin.site.register(Chat)
# admin.site.register(Group)
