from django.conf import settings
from django.db import models

class UserProfile(models.Model):
    ROLE_STUDENT = 'student'
    ROLE_PARENT = 'parent'

    ROLE_CHOICES = [
        (ROLE_STUDENT, 'Ученик'),
        (ROLE_PARENT, 'Родитель'),
    ]

    GRADE_CHOICES = [
        (8, '8 класс'),
        (9, '9 класс'),
        (10, '10 класс'),
        (11, '11 класс'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='profile')

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=ROLE_STUDENT,
        verbose_name='роль',
    )

    patronymic = models.CharField(max_length=100,blank=True,null=True,verbose_name="Отчество")

    bio=models.TextField(max_length=500,blank=True,null=True,verbose_name="О себе")

    avatar=models.ImageField(upload_to="avatars/",blank=True,null=True,verbose_name="аватар")

    grade=models.IntegerField(
        choices=GRADE_CHOICES,
        null=True,
        blank=True,
        verbose_name="класс",
    )

    target_score=models.IntegerField(null=True,blank=True,verbose_name="целевой балл ЕГЭ")

    created_at=models.DateTimeField(auto_now_add=True,verbose_name="Дата создание")

    updated_at=models.DateTimeField(auto_now=True,verbose_name="Дата обновления")

    class Meta:
        verbose_name="Профиль"
        verbose_name_plural="Профили"
        ordering=['-created_at']

    def __str__(self):
        return self.user.get_full_name() or self.user.username
