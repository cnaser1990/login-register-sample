from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import UserManager
# Create your models here.

class User(AbstractBaseUser):
    
    email=models.EmailField(max_length=255 , unique=True)
    full_name=models.CharField(max_length=255)
    
    is_permium=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)
    is_admin=models.BooleanField(default=False)
    
    USERNAME_FIELD='email'
    REQUIRED_FIELDS = ['full_name']
    
    objects=UserManager()
    
    def __str__(self):
        return self.email
    
    def has_perm(self , perm , obj=None):
        return True
    
    def has_module_perms(self , app_label):
        return True
    
    @property
    def is_staff(self):
        return self.is_admin
    
class OtpCode(models.Model):
    code=models.PositiveSmallIntegerField()
    email=models.EmailField()
    created=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.email}-{self.code}-{self.created}'