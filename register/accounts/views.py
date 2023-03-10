from django.shortcuts import render
from .forms import UserRegisterForm , UserLoginForm , VerifyCodeForm
from django.views.generic import View
from django.shortcuts import redirect
import random
from .models import User , OtpCode
from .utils import send_otp_code
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login , logout , authenticate
# Create your views here.

class UserRegisterView(View):
    form_class=UserRegisterForm
    template_name='register.html'
    
    def dispatch(self, request, *args, **kwargs) :
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self , request):
        form=self.form_class
        return render(request , self.template_name , {'form':form})
    
    def post(self , request):
        form=self.form_class(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            random_code=random.randint(1000,9999)
            OtpCode.objects.create(code=random_code , email=cd['email'])
            request.session['user_info']={
                
                'email':cd['email'],
                'full_name':cd['full_name'],
                'password':cd['password']
                                            }

            send_otp_code(cd['email'] , random_code)
            messages.success(request , 'یک کد برای شما ارسال کردیم .' , 'success')
            return redirect('accounts:verify_code')
        return render(request , self.template_name , {'form':form})
    
class UserRegisterVerifyCodeView(View):
    form_class = VerifyCodeForm
    template_name='verify.html'
    
    def dispatch(self, request, *args, **kwargs) :
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self , request):
        form = self.form_class
        return render (request , self.template_name , {'form':form})
    
    def post (self , request):
        user_session=request.session['user_info']
        code_instance=get_object_or_404( OtpCode , email=user_session['email'])
        form=self.form_class(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            if cd['code']==code_instance.code:
                User.objects.create_user(user_session['email'],user_session['full_name'],user_session['password'])
                code_instance.delete()
                # try:
                #     send_mail('ثبت نام', f'کاربر {user_session["email"]} ثبت نام کرد' , settings.EMAIL_HOST_USER ,['our email'],fail_silently=False)
                # except:
                #     pass
                messages.success(request , 'شما با موفقیت ثبت نام کردید!' , 'success')
                return redirect('accounts:login')
            messages.error(request ,'کد اشتباه است!','danger')
            return redirect('accounts:verify_code')
        return render (request , self.template_name , {'form':form})
    
class UserLogoutView(LoginRequiredMixin , View):
    def get(self , request):
        logout(request)
        messages.success(request , 'با موفقیت خارج شدید!' , 'success')
        return redirect('home:home')

class UserLoginView(View):
    form_class=UserLoginForm
    template_name='login.html'
    
    def setup(self, request, *args, **kwargs) :
        self.next=request.GET.get('next')
        return super().setup(request, *args, **kwargs)
    
    def dispatch(self, request, *args, **kwargs) :
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self , request):
        form=self.form_class
        return render(request , self.template_name , {'form':form})
    
    def post(self, request):
        form=self.form_class(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            user=authenticate(request ,email=cd['email'] , password=cd['password'] )
            if user is not None:
                login(request , user)
                messages.success(request , f'خوش آمدید {user.full_name}' , 'success')
                if self.next:
                    return redirect(self.next)
                return redirect('home:home')
            messages.error(request ,'ایمیل یا پسورد اشتباه است!','danger')
        return render (request , self.template_name , {'form':form})