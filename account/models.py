from datetime import datetime, timedelta

import jwt
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
import secrets

from afiche import settings


class UserManager(BaseUserManager):
    def _create(self, email, password, **extra_fields):
        if not email:
            raise ValidationError('Email cannot be blank')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.create_activation_code()
        user.set_password("qwe12345")
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault('is_active', False)
        extra_fields.setdefault('is_staff', False)
        return self._create(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        return self._create(email, password, **extra_fields)


class WorkPlace(models.Model):
    address = models.CharField(max_length=500)
    address_url = models.CharField(max_length=500, blank=True, null=True)

class UserAddress(models.Model):
    city = models.CharField(max_length=35, blank=True, null=True)
    region = models.CharField(max_length=35, blank=True, null=True)
    address = models.CharField(max_length=500, blank=True, null=True)

class Document(models.Model):
    name = models.CharField(max_length=35)
    document = models.FileField(upload_to='documents/')

    def get_pdf_url(self):
        try:
            pdf = getattr(self, 'document')
            if pdf:
                return f"{settings.LINK}{pdf.url}"
            else:
                return 'PDF Not Found'
        except ValueError:
            return 'PDF Not Found'


class UserModel(AbstractBaseUser):

    email = models.EmailField(unique=True, db_index=True)
    phone_number = models.CharField(max_length=20, unique=True)
    full_name = models.CharField(max_length=60)

    inn = models.CharField(max_length=100, null=True, blank=True)

    user_age = models.PositiveIntegerField(default=0)
    gender = models.PositiveIntegerField(default=0)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    user_rating = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    user_workplace = models.OneToOneField(WorkPlace, on_delete=models.CASCADE, blank=True, null=True)
    user_address = models.OneToOneField(UserAddress, on_delete=models.CASCADE, blank=True, null=True)

    user_avg_income = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    user_documents = models.ManyToManyField(Document, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'phone_number']
    
    activation_code = models.CharField(max_length=8, blank=True)
    objects = UserManager()

    def __str__(self):
        return f'{self.full_name}, {self.phone_number}'

    def create_activation_code(self):
        code = secrets.token_urlsafe(6)
        self.activation_code = code
        self.save()

    def has_module_perms(self, app_label):
        return self.is_staff

    def has_perm(self, perm, obj=None):
        return self.is_staff

    @property
    def token(self):
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=1)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')






