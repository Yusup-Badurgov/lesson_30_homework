from django.db import models

class Location(models.Model):
    name = models.CharField('Название', max_length=100, unique=True)
    lat = models.DecimalField('Латтитуда', max_digits=8, decimal_places=6, null=True, blank=True)
    lng = models.DecimalField('Лонгитуда', max_digits=8, decimal_places=6, null=True, blank=True)

    class Meta:
        verbose_name = 'Локация'
        verbose_name_plural = 'Локации'

    def __str__(self):
        return self.name



class UserRoles(models.TextChoices):
    MEMBER = 'member', 'Пользователь'
    MODERATOR = 'moderator', 'Модератор'
    ADMIN = 'admin', 'Админ'


class User(models.Model):
    first_name = models.CharField('Имя', max_length=150)
    last_name = models.CharField('Фамилия', max_length=150)
    username = models.CharField('Никнейм', max_length=100, unique=True)
    password = models.CharField('Пароль', max_length=50)
    role = models.CharField(choices=UserRoles.choices, max_length=9)
    age = models.PositiveSmallIntegerField()

    location = models.ManyToManyField(Location)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

