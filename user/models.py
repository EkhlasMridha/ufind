from django.db import models
from django.core.validators import EmailValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, name, password=None):
        user = self.model(
            email=self.normalize_email(email),
            name=name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        user = self.create_user(
            email=self.normalize_email(email),
            name=name,
            password=password
        )

        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser):
    username = None
    email = models.EmailField(verbose_name='email',
                              max_length=200, unique=True)
    name = models.CharField(max_length=200)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perm(self, app_label):
        return True
