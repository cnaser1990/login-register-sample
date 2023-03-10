from django import forms
from django.core.exceptions import ValidationError
from .models import User , OtpCode
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import gettext_lazy as _

# forms for admin panel
class UserCreationForm(forms.ModelForm):
    password1=forms.CharField(label='password' , widget=forms.PasswordInput)
    password2=forms.CharField(label='confirm password' , widget=forms.PasswordInput)
    
    class Meta:
        model=User 
        fields=['email' , 'full_name']
        
    def clean_password2(self):
        cd=self.cleaned_data
        if cd['password1'] and cd['password2'] and cd['password1'] != cd['password2']:
            raise ValidationError('passwords does not match !')
        return cd['password2']
    
    def save(self , commit=True):
        user=super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
    
class UserChangeForm(forms.ModelForm):
    password=ReadOnlyPasswordHashField(help_text='you can change your password from <a href="../password/">here</a>')
    class Meta:
        model=User
        fields=['email' , 'full_name' , 'password' , 'last_login']
        
        
# forms for site 

class UserRegisterForm(forms.Form):
    email=forms.EmailField(label=('ایمیل') , widget=forms.EmailInput(), error_messages={'required': _("ایمیل خود را وارد کنید !"),'invalid':_('این ایمیل صحیح نمی باشد !') , 'exists':_('این ایمیل از قبل وجود دارد!')})
    full_name=forms.CharField(min_length=6, max_length=100 , label=('نام و نام خانوادگی'),widget=forms.TextInput(), error_messages={'required': _(" نام و نام خانوادگی خود را وارد کنید !"),'invalid':_('این نام صحیح نمی باشد !'),'exists':_('این نام از قبل وجود دارد!'),'min_length': _('نام و نام خانوادگی حداقل باید 6 حرف باشد !')})
    password=forms.CharField(label=('پسورد') ,widget=forms.PasswordInput(),error_messages= {'required': _("پسورد خود را وارد کنید !"),'invalid':_('این پسورد صحیح نمی باشد !')}) 

    
    def clean_email(self):
        email=self.cleaned_data['email']
        user=User.objects.filter(email=email).exists()
        
        if user :
            raise ValidationError('این ایمیل از قبل وجود دارد!')
        OtpCode.objects.filter(email=email).delete()
        return email
    
    
    def clean_full_name(self):
        full_name=self.cleaned_data['full_name']
        user=User.objects.filter(full_name=full_name).exists()
        
        if user :
            raise ValidationError('این نام کاربری از قبل وجود دارد!')
        return full_name 
    
    def clean_password(self):
        password=self.cleaned_data['password']
        
        if len(password) < 8 :
            raise ValidationError('پسورد حداقل باید 8 حرف باشد!')
        
        
        return password
        
class VerifyCodeForm(forms.Form):
    code=forms.IntegerField(label=('کد'),widget=forms.TextInput(),error_messages={'required': _("کد را وارد کنيد!")})  
    
class UserLoginForm(forms.Form):
    email=forms.EmailField(label=('ایمیل') , widget=forms.EmailInput() , error_messages={'required': _("ایمیل خود را وارد کنید !"),'invalid':_('این ایمیل صحیح نمی باشد !')})
    password=forms.CharField(label=('پسورد') ,widget=forms.PasswordInput(), error_messages= {'required': _("پسورد خود را وارد کنید !"),'invalid':_('این پسورد صحیح نمی باشد !')}) 
