from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from datetime import timedelta
from django.utils import timezone
# Create your models here.
class UserAccountManager(BaseUserManager):
    use_in_migrations = True
    def create_user(self, email,password,first_name,last_name,username):
        if not email:
            raise ValueError('Email must be set!')
        user = self.model(email=email)
        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email,password,first_name='admin',last_name='admin',username=None)
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

    # def get_by_natural_key(self, email):
    #     return self.get(code_number=email)



class User(AbstractBaseUser, PermissionsMixin):
    MY_CHOICES = (
        ('Neutral','Neutral'),
        ('At Capacity', 'At Capacity'),
        ('Looking For Work','Looking For Work'),
    )
    email = models.EmailField(
        unique=True,
        max_length=254,
    )
    first_name = models.CharField(max_length=15,blank=True)
    last_name = models.CharField(max_length=15,blank=True)
    status = models.CharField(max_length=50,choices=MY_CHOICES,default='Neutral')
    is_active_status = models.BooleanField(default=False)
    timeout_flag = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_by_natural_key(self, email_):
        return self.get(code_number=email_)


    
