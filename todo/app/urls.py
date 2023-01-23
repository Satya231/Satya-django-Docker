from django.contrib import admin
from django.urls import path
# from app.views import home, login , signup , add_todo , signout , delete_todo, change_todo, change_password,verify, forget_password,verify1,password_reset,Resend_otp,update_todo,index
from django.contrib.auth import views as auth_views
from .views import*
#resend_otp


urlpatterns = [
   path('' , home, name='home' ),
   #path('', TodoAPI.as_view(), name='home' ),
   path('signup/', signup, name='signup'),
   #path('signup/', SignupView.as_view(), name='signup'),
   #  path('login/', LoginView.as_view(),name='login'), 
   path('login/' ,login , name='login'), 
   # path('signup/' , signup, name='signup' ), 
   path('add-todo/' , add_todo, name='add-todo' ), 
   path('update-todo/<int:id>/', update_todo, name = 'update'),
   path('delete-todo/<int:id>/' , delete_todo ), 
   path('change-status/<int:id>/<str:status>/' , change_todo ), 
   path('logout/' , signout ),
   path('changepass/', change_password, name='changepass'),
   path('Resend_Otp/', Resend_otp, name='Resend_Otp'),
   path('verify/', verify, name='verify'),
   path('forget_password/', forget_password, name='forget_password'),
   path('verify1/', verify1, name='verify1'),
   path('password_reset/', password_reset, name='password_reset'),
    #path('index/', index),
   #path("celery_tasks/", test, name='test')
]