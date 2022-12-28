from django.shortcuts import render , redirect,HttpResponse
import os
from django.http import HttpResponse
from django.contrib.auth import authenticate , login as loginUser  , logout
from django.contrib.auth.forms import AuthenticationForm , PasswordChangeForm
# Create your views here.
from app.forms import TODOForm,signupForm,SetPasswordForm,forget_passwordForm,Password_rest_form,UserLoginForm, UpdateForm
from app.models import TODO,MyCustomModel,user_otp
from django.contrib.auth.decorators import login_required
import random
import json
from django.conf import settings
from django.contrib import messages
from .tasks import send_email, extract_text, file_validation
from celery.contrib import rdb
from todo import settings
from .Text_extraction import extract
from PIL import Image
from celery import chain
import os.path
import ipdb





#=======================================================Home View Page===========================================================================================
''' This Is Home Page To Display All The Actions of Todo
     here we have applied filter the query set for user object of Model TODO to Display All the Field's Value Related to User
      and set ordering is by priority'''

@login_required(login_url='login')
def home(request):
    if request.user.is_authenticated:
        user = request.user
        form = TODOForm()
        todos = TODO.objects.filter(user = user).order_by('priority')

        return render(request , 'index.html' , context={'form' : form , 'todos' : todos,   })
    else:
            return redirect('login')



#==========================Sign_Up Verification via OTP=============================================================================================
''' After validating form of signup page we set user to inactive mode, so that users can't able to login.
     Because without Email Otp Verification Users can't login .and also we are setting a session id for user to validating next page.
     Here we also calling Otp function to generate otp and create a new object for user_otp to store user and otp in backend and 
     also calling Send_email function where we are sending otp to email.
     After signup form,page will redirected To Otp Verification Page  '''
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
            email = user.email
            if user is not None:
                ur_otp=otp()
                print(ur_otp)
                usr_otp = user_otp.objects.create(user =user, otp= ur_otp)
                usr_otp.save()
                
                usr = MyCustomModel.objects.get(id = user_id)
                send_email.apply_async(args=[email, ur_otp])
                
                messages.success(request, f'Otp Has Sent Successfully To Ur Mail.Check Ur Mail')
            return render(request, 'otp_check.html', {'otp':True, 'usr':user})
        else:
            return render(request , 'signup.html' , context=context)


# def send_mail_func(request):
#     send_email(user_id)
#     return HttpResponse("sent")
#==================================================Login Functions=============================================================================================================
''' here after getting Post req ,validating Form and save the user.
    Setting a SESSION id for  user for validating in nxt page.
    and finally redirected  to home page after valid login'''

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
                #request.session['uid'] = request.POST.get('user.id') 
                return redirect('home')
        else:
            context = {
                "form" : form
            }
            return render(request , 'login.html' , context=context )




''' Here we have just made an otp function to generate otp by using Random module'''

def otp():
    return random.randint(100000,999999)


#=============================================Resend Otp  ================================================================================================================

def Resend_otp(request):
    
    if request.method == "GET":
        temp = request.session['uid']
        print(temp)
        get_usr = MyCustomModel.objects.filter(id = temp)
        print(get_usr)

        if get_usr.exists(): 
            user = MyCustomModel.objects.get(id = temp)
            user_id = user.id
            usr_otp = user_otp.objects.filter(user = user) 
            if usr_otp:
                usr_otp = user_otp.objects.get(user = user)
                
                my_otp = otp()
                usr_otp.otp = my_otp
                usr_otp.save()
                print(usr_otp.otp)

                
                #send_mail_func(user.id)
                #messages.success(request, f'Otp Has ReSent Successfully To Ur Mail.Check Ur Mail')
               
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
        
            if int(get_otp) == user_otp.objects.filter(user=usr).first().otp:
                usr.is_active = True
                usr.save()
                messages.success(request, f'Account is Created For {usr.email}')

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
            #image = request.FILES.get('image')
           
            todo = form.save(commit=False)
            todo.user = user
            todo.save()
            image = todo.image.path
            print("abcd")
            print(image)

            todo1 = TODO.objects.filter(user = request.user)
            #ipdb.set_trace()
            if todo1:
                
                ''' Image_field's value extraction and save extracted text into TODO text field '''

                #field_name = 'image'
                obj = TODO.objects.last()
                
                # image_file = getattr(obj, field_name)
                
                # obj_1 = TODO.objects.values().last()
                # image = obj_1['image']
                
                # id = obj_1['id']
                # print(image)
                # print("abcd")
                # text = extract(img_file)
                # payload = {'image':'files'}
                #file_name = json.dumps('image')
    
                text = chain(file_validation.s(image),extract_text.s()).apply_async()
                
                print(text.get())
                obj.text = text.get()
            
                obj.save()
                          
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
            #import ipdb;ipdb.set_trace()
            user = MyCustomModel.objects.get(email=email)
            user.is_active = False
            user.save()
            user_id = user.id
            request.session['email'] = request.POST['email']
            if user is not None:

                    
                #user = MyCustomModel.objects.get(user=user_id)
                #user_otp.otp = my_otp
                #user_otp.save()
                #import ipdb;ipdb.set_trace()
                usr_otp = user_otp.objects.filter(user =user)
                if usr_otp:
                    usr_otp = user_otp.objects.get(user = user)
                    #import ipdb;ipdb.set_trace()
                    my_otp = otp()
                    #print(my_otp)
                    usr_otp.otp = my_otp
                    usr_otp.save()
                    print(usr_otp.otp)
                    #usr = MyCustomModel.objects.get(id = user_id)
                    email = user.email
                    print(email)
                    #json_email = json.dumps(email)
                    #print(json_email)
                    #json_otp = json.dumps(my_otp)
                    #user = user_otp.objects.get(user=user)
                    # print(user_otp)
                    #import ipdb;ipdb.set_trace()
                    send_email.apply_async(args=[email, my_otp])
                    
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

            if int(get_otp) == user_otp.objects.filter(user=usr).first().otp:
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

#================websocket connections====================================================================================================================================

# def test(request):
#    test_func.delay()
#    return HttpResponse("Done") 

    
    
        