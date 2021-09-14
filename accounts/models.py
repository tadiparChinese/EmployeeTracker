from django.db import models

# Create your models here.

from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, name, password, user_name, mobile=None, email=None):
        user = self.model(name=name, email=self.normalize_email(email), user_name=user_name)
        user.set_password(password)
        user.is_active = True
        user.save()
        return user

    def create_superuser(self, password, mobile, name):
        user = self.model(name=name, mobile=mobile)
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save()
        return user

class EmployeeAccount(AbstractBaseUser, PermissionsMixin):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.EmailField(blank=True, null=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    signup_date = models.DateField(auto_now_add=True)
    user_name = models.CharField(max_length=100, unique=True)

    USERNAME_FIELD = 'user_name'

    objects = UserManager()

    def __str__(self):
        return "{}".format(self.id)

    def __id__(self):
        return self.id

    class Meta:
        # db_table = 'employee_account'
        managed = True


class EmployeeInfo(models.Model):
    employee = models.ForeignKey(EmployeeAccount, on_delete=models.CASCADE)
    login_datetime = models.DateTimeField(auto_now_add=True)
    logout_datetime = models.DateTimeField(null=True, blank=True)
    hours = models.SmallIntegerField(default=0)
    minutes = models.IntegerField(default=0)
    created_date = models.DateField(auto_now_add=True)
