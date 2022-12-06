from django.shortcuts import render , redirect,HttpResponse,HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth import authenticate , login as loginUser  , logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm , PasswordChangeForm
# Create your views here.
from app.forms import TODOForm,signupForm,SetPasswordForm,forget_passwordForm,Password_rest_form,UserLoginForm, UpdateForm
from app.models import TODO,MyCustomModel,user_otp
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
import random
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .utils import send_email
from django.contrib.auth import get_user_model
from functools import lru_cache
from django.views.decorators.cache import cache_page
from todo import settings


#=======================================================Home View Page===========================================================================================

@login_required(login_url='login')
def home(request):
    if request.user.is_authenticated:
        user = request.user
        form = TODOForm()
        todos = TODO.objects.filter(user = user).order_by('priority')
        #print(todos.__dict__)
        # if (request.session.has_key('uid')):
        #     res = request.session['uid']
        #     print(res)
        return render(request , 'index.html' , context={'form' : form , 'todos' : todos, })
    else:
            return redirect('login')
''' This Is Home Page To Display All The Field's value Related to Todo
     here we have applied filter the quesry set for user of Model TODO to Display All the Field's Value Related to User
      and set ordering is by priority'''

#==================================================Login Page=============================================================================================================
def login(request):
    
    if request.method == 'GET':
        form1 = UserLoginForm()
        context = {
            "form" : form1
        }
        return render(request , 'login.html' , context=context )
    else:
        form = UserLoginForm(data=request.POST)
        print(form.is_valid())
        
        if form.is_valid():
            eml = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            data=request.POST.get('username')
            #print(data)
            user = authenticate(email=eml , password = password)
        

            if user is not None:
                loginUser(request , user)
                messages.success(request, f'You Have Logged In Successfully ')
                request.session['uid'] = request.POST.get('user.id') 
                return redirect('home')
        else:
            context = {
                "form" : form
            }
            return render(request , 'login.html' , context=context )

''' here after getting Post req ,validating Form and save the user.
    Setting a SESSION id for  user for validating in nxt page.
    and finally redirected  to home page after valid login'''

#==========================Sign_Up Verification via OTP=============================================================================================

def signup(request):

    if request.method == 'GET':
        form = signupForm()
        context = {
            "form" : form
        }
        return render(request , 'signup.html' , context=context)
    else:
        #print(request.POST)
        form = signupForm(request.POST)  
        context = {
            "form" : form
        }
        if form.is_valid():
            user = form.save()
            user.is_active=False  #now user is not active thus can,t login bec we have to verify user with OTP
            user.save()
            user_id = user.id
            request.session['uid'] = user_id
            print(user)
            if user is not None:
                my_otp=otp()
                print(my_otp)
                usr_otp = user_otp.objects.create(user =user, otp= my_otp)
                usr_otp.save()
                #send_email(user_id)
                messages.success(request, f'Otp Has Sent Successfully To Ur Mail.Check Ur Mail')
            return render(request, 'otp_check.html', {'otp':True, 'usr':user})
        else:
            return render(request , 'signup.html' , context=context)

''' After validating form of signup page we set users in inactive mode, so that users cant able to login.
     Because without Email Otp Verification Users can't login .and also we are setting a session id for user to validating next page.
     Here we also calling Otp function to generate otp and create a new object for user_otp to store user and otp in backend and 
     also calling Send_email function where we are sending otp to email.
     After signup form,page will redirected To Otp Verification Page  '''



def otp():
    return random.randint(100000,999999)
''' Here we have just made an otp function to generate otp by using Random module'''
#=============================================Resend Otp  ================================================================================================================

def Resend_otp(request):
    
    if request.method == "GET":
        temp = request.session['uid']
        print(temp)
        get_usr = MyCustomModel.objects.filter(id = temp)
        print(get_usr)

        if get_usr.exists(): 
            user = MyCustomModel.objects.get(id = temp)
            usr_otp = user_otp.objects.filter(user = user) 
            if usr_otp:
                usr_otp = user_otp.objects.get(user = user)
                my_otp = otp()
                usr_otp.otp = my_otp
                usr_otp.save()
                print(usr_otp.otp)

                mess = f"Hello {user.username},\nYour OTP is {usr_otp.otp}\nThanks!"
                # send_mail(
                #     "Welcome to My ToDo - Verify Your Email",
                #     mess,
                #     settings.EMAIL.HOST_USER,
                #     [get_usr.email],
                #     fail_silently = False

                # )
            return render(request, 'otp_check.html', {'otp':True, 'usr':user})
    return HttpResponse("Cant't Send")



#==================================SignUp OTP Verif.=================================================================================================

def verify(request):
    if request.method == 'POST':
        get_otp = request.POST.get('otp')
        if get_otp:
            get_usr = request.POST.get('usr')
            #usr = MyCustomModel.objects.get(email=request.POST.get('email'))
            usr = MyCustomModel.objects.get(email = get_usr)
        
            if int(get_otp) == user_otp.objects.filter(user=usr).last().otp:
                usr.is_active = True
                usr.save()
                messages.success(request, f'Account is Created For {usr.username}')

                return redirect('login')
            else:
                messages.warning(request, f'You Entered a Wrong OTP')
                return render(request, 'otp_check.html', {'otp': True, 'usr': usr})
        




#=====================================CRUD OPerations=============================================================================================================
@login_required(login_url='login')
def add_todo(request):
    if request.user.is_authenticated:
        user = request.user
        #print(user)
        form = TODOForm(request.POST,request.FILES)
        #print(request.POST, request.FILES) 
        if form.is_valid():
            print(form.cleaned_data)
            todo = form.save(commit=False)
            todo.user = user
            todo.save()
            #print(todo)
            return redirect("home")
        else: 
            return render(request , 'index.html' , context={'form' : form})

@login_required(login_url='login')
def update_todo(request, id):
   if request.user.is_authenticated:
    user = request.user  
    obj = TODO.objects.get(pk = id)
    form =  UpdateForm(request.POST,request.FILES, instance=obj)
    if form.is_valid():
        todo = form.save()
        todo.user = user
        todo.save()
        return redirect("home")
    else:
        form =  UpdateForm(instance=obj)
        context = {'form':form}
        return render(request, 'updateview.html', context)


def delete_todo(request , id ):
    print(id)
    TODO.objects.get(pk = id).delete()
    return redirect('home')

def change_todo(request , id  , status):
    todo = TODO.objects.get(pk = id)
    todo.status = status
    todo.save()
    return redirect('home')


@login_required(login_url='login')
def change_password(request ):
    if request.user.is_authenticated:
        if request.method == 'POST':
            fm = PasswordChangeForm(user=request.user, data = request.POST)
            if fm.is_valid():
                fm.save()
                #update_session_auth_hash(request, fm.user)
            return redirect('home')
        else:
            fm = PasswordChangeForm(user = request.user)
        #user = request.user
        return render(request, 'changepass.html', {'form': fm})




def signout(request):
    request.session.clear()
    logout(request)
    return redirect('login')


#============================================Reset Password via OTP==========================================================================================================

def forget_password(request):
    if request.method == 'GET':
        form = forget_passwordForm()
        context = {
            "form" : form
        }
        return render(request , 'forget_password.html' , context=context)
    else:
        form = forget_passwordForm(request.POST)
        
        email = request.POST.get('email')
        user_email = MyCustomModel.objects.filter(email = email)
        if user_email:
            user = MyCustomModel.objects.get(email=email)
            user.is_active = False
            user.save()
            user_id = user.id
            request.session['email'] = request.POST['email']
            if user is not None:

                    
                    #user = MyCustomModel.objects.get(user=user_id)
                    #user_otp.otp = my_otp
                    #user_otp.save()
                    usr_otp = user_otp.objects.filter(user =user)
                    if usr_otp:
                        usr_otp = user_otp.objects.get(user = user)
                        my_otp = otp()
                        usr_otp.otp = my_otp
                        usr_otp.save()
                        print(usr_otp.otp)
                        #send_email(user_id)
                        messages.success(request, f'Otp Has Sent Successfully To Ur Mail.Check Ur Mail')
                    return render(request, 'otp_check1.html', {'otp':True, 'usr':user})
        else:
            messages.warning(request,f'invalid user_email, pln enter correct email')
            return render(request, 'forget_password.html', {'form':form})


#===========================================Reset PassWord Verif.=============================================================================================


def verify1(request):
     if request.session.has_key('email'):
        email = request.session['email']
        get_otp = request.POST.get('otp')
        if get_otp:
            get_usr = request.POST.get('usr')
            usr = MyCustomModel.objects.get(email=get_usr)

            if int(get_otp) == user_otp.objects.filter(user=usr).last().otp:
                usr.is_active = True
                usr.save()
                messages.success(request, f'your Email is verified')
                return redirect('password_reset')
            else:
                messages.warning(request, f'you have entered a wrong otp')
                return render(request, 'otp_check1.html', {'otp':True, 'usr': usr})


#======================================================Forget Password Reset==========================================================================================================

def password_reset(request):
    if request.session.has_key('email'):
        email = request.session['email']
        print(email)
        user = MyCustomModel.objects.get(email=email)
        if request.method == 'POST':
            form = Password_rest_form(request.POST)
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            if not new_password:
                messages.warning(request, f'Enter New Password')
            elif not confirm_password:
                messages.warning(request,f'plz Enter Your Confirm Password')
            elif new_password == user.password:
                messages.warning(request, f'Password Already Exists!!!!!Plz Enter New Password ')
            elif new_password != confirm_password:
                messages.warning(request, f'Password is not matched')
            else: 
                
                user.set_password(new_password)
                user.save()
                messages.success(request,f'Password changed successfully')
                return redirect('login')
        else:
            form = Password_rest_form()
            return render(request, 'password_reset.html', {'form':form})


            

    
    
        