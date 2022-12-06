from django import forms
#from django.forms import ModelForm
from .models import TODO,MyCustomModel
from django.contrib.auth import authenticate,password_validation,get_user_model
from django.contrib.auth.forms import UserCreationForm,SetPasswordForm
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator




''' ToDo Form  with Image File Validators'''
class TODOForm(forms.ModelForm):
    image = forms.FileField(validators=[FileExtensionValidator(['png','jpg','webp'])])
    class Meta:
        model = TODO
        fields = ['tasks' , 'status' ,'image', 'priority']

        def clean_img(self):
            image = self.cleaned_data.get("image")
            if not image:
                raise ValidationError("Image Is Required")

            return image

''' Update Form Inheriting Todo Form For Updating All The Fields'''
class UpdateForm(TODOForm):
    class Meta:
        model = TODO
        fields = ['tasks'  ,'image', 'priority']



class signupForm(UserCreationForm):
    #email = forms.EmailField()
    class Meta:
        model = MyCustomModel
        fields = ("email",)

''' This Is For Email Field Where We'll Verify Our Email'''
class forget_passwordForm(forms.ModelForm):
    email = forms.EmailField(max_length=125)
    class Meta:
        model = MyCustomModel
        fields = ["email",]
        
'''This Is For Password Reset Field After Verifying Email With Otp  Clicking Forget password'''
class Password_rest_form(forms.Form):
    new_password = forms.CharField(max_length=100, widget = forms.PasswordInput)
    confirm_password = forms.CharField(max_length=100, widget = forms.PasswordInput)



''' Custom User Login Form'''
class UserLoginForm(forms.Form):
    email=forms.EmailField(max_length = 100)
    password=forms.CharField()

    def clean(self,*args,**kwargs):
        email=self.cleaned_data.get('email')
        password=self.cleaned_data.get('password')

        if email and password:
            user=authenticate(username=email,password=password)

            if not user:
                raise forms.ValidationError('User Does Not Exist')
            
            if not user.check_password(password):
                raise forms.ValidationError('Incorrect Password')
        
        return super(UserLoginForm, self).clean(*args,**kwargs)

user=get_user_model()
    
       



# class PasswordUpdateForm(signupForm):
#     class Meta:
#         models = MyCustomModel
#         fields = ('password',)






# class forget_pass_form(SetPasswordForm):
#     field_order = [ "new_password1", "new_password2"]



    
# class LoginForm(forms.ModelForm):
#     """
#       Form for Logging in  users
#     """
#     password  = forms.CharField(label= 'Password', widget=forms.PasswordInput)
    

#     class Meta:
#         model  =  MyCustomModel
#         fields =  ('email', 'password',)


#         def clean(self):
#             if self.is_valid():

#                 email = self.cleaned_data.get('email')
#                 password = self.cleaned_data.get('password')
#                 if not authenticate(email=email, password=password):
#                     raise forms.ValidationError('Invalid Login')


    


# class MytodoItemCreateForm(forms.ModelForm):
    
#      class Meta:
#          model = todo_list
#          fields = ('tasks', 'action' )
         


# class MytodoItemUpdateForm(forms.ModelForm):

# #     class Meta:
# #         model = MyCustomModel
# #         fields = ('name',)

