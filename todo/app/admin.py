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
    list_display = ('user', 'priority', 'tasks', 'status','image')

    ordering =('priority',)


class CustomUserAdmin(UserAdmin):
    
  
    model = MyCustomModel
    list_display = ('email','username', 'date_joined', 'is_staff', 'is_active',)
    add_fieldsets = (
    (None, {
        'classes': ('wide',),
        'fields': ('email', 'first_name', 'last_name', 'password1', 'password2'),
    }),
    )

   
    
    ordering = ('email',)


admin.site.register(TODO, TodoAdmin)
admin.site.register(MyCustomModel,CustomUserAdmin)
admin.site.register(user_otp,user_otpAdmin)
