from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.conf import settings
import jwt
from datetime import datetime, timedelta

# Create your models here.
class Advisor(models.Model):
    advisor_name = models.CharField(max_length=100)
    advisor_photo_url = models.URLField(max_length=1000)

    def __str__(self):
        return self.advisor_name


class MyUserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):

        user = self.create_user(
            email,
            password=password,
            username=username,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    username = models.CharField(max_length=50, verbose_name='name')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    @property
    def token(self):
        return self.generate_jwt_token()

    def generate_jwt_token(self):
        dt = datetime.now() + timedelta(minutes=60)

        token = jwt.encode({
            'id': self.pk,
            'exp': dt
        }, settings.SECRET_KEY, algorithm='HS256')

        return token


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    advisor = models.ForeignKey(Advisor, on_delete=models.CASCADE, related_name='advisor')
    date_time = models.DateTimeField()

    def __str__(self):
        return str(self.user)

