from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator
from django.db.models import Q
from django.db.models.signals import pre_save, post_save
# from blissedmaths.utils import unique_otp_generator
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save

import random
import os
import requests

class UserManager(BaseUserManager):
    # def create_user(self, phone, name, email, gender, dob, password=None,  is_staff=False, is_active=True, is_admin=False):
    def create_user(self, phone, password=None, **extra_fields):

        if not phone:
            raise ValueError('users must have a phone number')
        if not password:
            raise ValueError('user must have a password')

        user_obj = self.model(
            phone=phone, **extra_fields
        )
        user_obj.set_password(password)
        # user_obj.staff = is_staff
        # user_obj.admin = is_admin
        # user_obj.active = is_active
        # user_obj.name = name
        # user_obj.email = email
        # user_obj.gender = gender
        # user_obj.dob = dob
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, phone, password=None):
        user = self.create_user(
            phone,
            password=password,
            staff=True,


        )
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None):
        user = self.create_user(phone, password)
        user.staff=True
        user.is_superuser=True
        user.active=True
        user.user_type = 3
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    admin = 0
    nurse = 1
    runner = 2
    customer = 3
    user_type = [
        (admin, 'Admin'),
        (nurse, 'Nurse'),
        (runner, 'Runner'),
        (customer, 'User')
    ]
    phone_regex = RegexValidator( regex   =r'^\+?1?\d{9,14}$', message ="Phone number must be entered in the format: '+999999999'. Up to 14 digits allowed.")
    phone       = models.CharField(validators=[phone_regex], max_length=17, unique=True)
    name        = models.CharField(max_length = 20, blank = True, null = True)
    # standard    = models.CharField(max_length = 3, blank = True, null = True)
    # score       = models.IntegerField(default = 16)
    first_login = models.BooleanField(default=False)
    active      = models.BooleanField(default=True)
    staff       = models.BooleanField(default=False)
    admin       = models.BooleanField(default=False)
    timestamp   = models.DateTimeField(auto_now_add=True)
    email       = models.CharField(max_length = 40, blank = True, null = True)
    dob         = models.CharField(max_length = 40, blank = True, null = True)
    gender      = models.IntegerField(default=0)
    is_account_activate = models.BooleanField(default=False)
    is_family_member = models.BooleanField(default=False)
    primary_user_ref = models.CharField(max_length=20, blank = True, null = True, default='')
    user_type = models.IntegerField(choices=user_type, default=customer,)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.phone

    def get_full_name(self):
        return self.phone

    def get_short_name(self):
        return self.phone

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):

        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active
    
   



def upload_image_path_profile(instance, filename):
    new_filename = random.randint(1,9996666666)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "profile/{new_filename}/{final_filename}".format(
            new_filename=new_filename,
            final_filename=final_filename
    )
         

def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


class Profile(models.Model):
    user            =   models.OneToOneField(User, on_delete= models.CASCADE)
    email           =   models.EmailField( blank = True, null = True)
    image           =   models.ImageField(upload_to = upload_image_path_profile, default=None, null = True, blank = True)
    address         =   models.CharField(max_length = 900, blank = True, null = True)
    city            =   models.CharField(max_length = 30, blank = True, null = True)
    first_count     =   models.IntegerField(default=0, help_text='It is 0, if the user is totally new and 1 if the user has saved his standard once' )

    def __str__(self):
        return str(self.user) 


class AddressList(models.Model):
    title = models.CharField(max_length = 200, blank = True, null = True, default='')
    user = models.ForeignKey(User, on_delete=models.CASCADE, default='')
    city = models.CharField(max_length = 30, blank = True, null = True)
    country = models.CharField(max_length = 30, blank = True, null = True)
    area = models.CharField(max_length = 100, blank = True, null = True)
    address1 = models.CharField(max_length = 200, blank = True, null = True)
    pincode = models.IntegerField(default=1)


def user_created_receiver(sender, instance, created, *args, **kwargs):
    if created:
        Profile.objects.get_or_create(user = instance)
post_save.connect(user_created_receiver, sender = User)



class PhoneOTP(models.Model):
    phone_regex = RegexValidator( regex   =r'^\+?1?\d{9,14}$', message ="Phone number must be entered in the format: '+999999999'. Up to 14 digits allowed.")
    phone       = models.CharField(validators=[phone_regex], max_length=17, unique=True)
    otp         = models.CharField(max_length = 9, blank = True, null= True)
    count       = models.IntegerField(default = 0, help_text = 'Number of otp sent')
    logged      = models.BooleanField(default = False, help_text = 'If otp verification got successful')
    forgot      = models.BooleanField(default = False, help_text = 'only true for forgot password')
    forgot_logged = models.BooleanField(default = False, help_text = 'Only true if validdate otp forgot get successful')


    def __str__(self):
        return str(self.phone) + ' is sent ' + str(self.otp)


