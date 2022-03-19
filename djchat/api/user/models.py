from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
 
 
class UserManager(BaseUserManager):
    def _create_user(self, email, username, password, **extra_fields):
        if not email: 
            raise ValueError("Вы не ввели Email")
        if not username:
            raise ValueError("Вы не ввели Логин")
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, email, username, password):
        return self._create_user(email, username, password)
 
    def create_superuser(self, email, username, password):
        return self._create_user(email, username, password, is_staff=True, is_superuser=True)


class User(AbstractBaseUser, PermissionsMixin):
    st = [(0,'Почта'),(1,'Логин'), (2, "Имя и фамилия")]

    username = models.CharField("Логин", max_length=50, unique=True)
    email = models.EmailField("Почта", max_length=100, unique=True)
    is_active = models.BooleanField("Статус активации", default=True)
    is_staff = models.BooleanField("Статус админа", default=False)

    first_name = models.CharField('Имя', max_length=30, blank=True, default="Анонимный")
    last_name = models.CharField('Фамилия', max_length=30, blank=True, default="Пользователь")
    display_name = models.IntegerField("Имя пользователя на сайте", choices=st, default=0)
    photo = models.ImageField("Аватар", upload_to="user")
    link_network = models.CharField("Ссылка на профиль в соц.сети", max_length=50)
    phone_number = models.CharField("Номер телефона", max_length=25)

    date_joined = models.DateTimeField('Дата регистрации', auto_now_add=True)
    mail_tempkey = models.CharField("Временный ключ", max_length=30, blank=True)
    
    USERNAME_FIELD = 'email' # Идентификатор для обращения 
    REQUIRED_FIELDS = ['username'] # Список имён полей для Superuser
 
    objects = UserManager() # Добавляем методы класса MyUserManager
    
    def get_display_name(self):
        if self.display_name == 0:
            return self.email
        elif self.display_name == 1:
            return self.username
        else:
            return f"{self.first_name} {self.last_name[0]}."

    def __str__(self):
        return self.get_display_name()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'