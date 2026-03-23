from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='profile')

    patronymic = models.CharField(max_length=100,blank=True,null=True,verbose_name="Отчество")

    bio=models.TextField(max_length=500,blank=True,null=True,verbose_name="О себе")

    avatar=models.ImageField(upload_to="avatars/",blank=True,null=True,verbose_name="аватар")

    GRADE_CHOICES = [
    (10,"10 класс"),
    (11,"11 класс"),
    ]

    grade=models.IntegerField(choices=GRADE_CHOICES,default=10,verbose_name="класс")

    target_score=models.IntegerField(null=True,blank=True,verbose_name="целевой балл ЕГЭ")

    created_at=models.DateTimeField(auto_now_add=True,verbose_name="Дата создание")

    updated_at=models.DateTimeField(auto_now=True,verbose_name="Дата обновления")

    class Meta:
        verbose_name="Профиль"
        verbose_name_plural="Профили"
        ordering=['-created_at']

    def __str__(self):
        return self.user.get_full_name()
