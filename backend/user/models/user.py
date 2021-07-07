from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class ROLE:
        SEEKER = 'seeker'
        EMPLOYER = 'employer'
        CHOICES = (
            (SEEKER, 'Соискатель'),
            (EMPLOYER, 'Работодатель'),
        )

    class SEX:
        MALE = 'male'
        FEMALE = 'female'
        CHOICES = (
            (MALE, 'Мужской'),
            (FEMALE, 'Женский'),
        )

    role = models.CharField(max_length=16, default=ROLE.SEEKER, choices=ROLE.CHOICES, verbose_name='Роль')
    phone = models.CharField(max_length=16, blank=True, null=True, verbose_name='Телефон')
    # first_name = models.CharField(_('first name'), max_length=150, blank=True)
    # middle_name = models.CharField(_('middle name'), max_length=150, blank=True)
    # last_name = models.CharField(_('last name'), max_length=150, blank=True)
    birthdate = models.DateTimeField(auto_now=False, auto_now_add=False, verbose_name='Дата рождения', blank=True, null=True)
    sex = models.CharField(max_length=16, blank=True, null=True, choices=SEX.CHOICES, verbose_name='Пол')
    # city = models.ForeignKey(City, )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        default_related_name = 'users'
