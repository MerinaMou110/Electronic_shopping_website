from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

class UserManager(BaseUserManager):
    def create_user(self, email, name, first_name, last_name, tc, role='user', password=None, password2=None):
        if not email:
            raise ValueError('User must have an email address')
        user = self.model(
            email=self.normalize_email(email),
            name=name,
            first_name=first_name,
            last_name=last_name,
            tc=tc,
            role=role,
        )
        user.set_password(password)
        user.is_active = False  # User is inactive until they click the activation link
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, first_name, last_name, tc, password=None):
        user = self.create_user(
            email,
            password=password,
            name=name,
            first_name=first_name,
            last_name=last_name,
            tc=tc,
            role='superadmin',
        )
        
        user.is_active = True  # Superuser should be active by default
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('admin', 'Admin'),
        ('superadmin', 'Superadmin'),
    ]

    email = models.EmailField(verbose_name='Email', max_length=255, unique=True)
    name = models.CharField(max_length=200)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    tc = models.BooleanField()
    is_active = models.BooleanField(default=False)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'first_name', 'last_name', 'tc']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.role == 'admin' or self.role == 'superadmin'

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.role == 'admin' or self.role == 'superadmin'
