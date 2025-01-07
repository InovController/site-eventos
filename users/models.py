from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import MaxValueValidator, MinValueValidator
        

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('O endereço de email deve ser fornecido')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    email = models.EmailField(max_length=100, unique=True)
    company = models.CharField(max_length=100)

    phone_regex = RegexValidator(
        regex=r'^\(\d{2}\) \d{5}-\d{4}$',
        message="O número de telefone deve estar no formato: (__) 00000-0000."
    )
    phone = models.CharField(
        validators=[phone_regex],
        max_length=15,  # Inclui espaço para parênteses, espaços e hífen
        unique=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'company', 'phone']
    username = None
    objects = CustomUserManager()
    
    def __str__(self):
        return self.email