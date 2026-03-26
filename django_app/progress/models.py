from django.conf import settings
from django.db import models
from django.db.models import UniqueConstraint


class Enrollment(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='enrollment')

    subject=models.ForeignKey("courses.Subject",on_delete=models.CASCADE,related_name="enrollment")

    enrolled_at=models.DateTimeField(auto_now_add=True,verbose_name="Дата поступления")

    class Meta:
        UniqueConstraint(fields=['user','subject'],name='unique_user_subject')

        verbose_name='Запись на курс'

        verbose_name_plural='Записи на курсы'

class UserProgress(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='progress')

    node=models.ForeignKey("courses.RoadmapNode",on_delete=models.CASCADE,related_name="user_progress")

    STATUS_CHOICES=[
        ("in_progress","In_progress"),
        ("complete","Complete"),
    ]
    status=models.CharField(max_length=100,choices=STATUS_CHOICES,default='in_progress',verbose_name="Статус")

    score=models.IntegerField(default=0,verbose_name="Набранные баллы")

    completed_at=models.DateTimeField(null=True,blank=True,verbose_name="Дата окончания")

    created_at=models.DateTimeField(auto_now_add=True,verbose_name="Дата создания")

    updated_at=models.DateTimeField(auto_now=True,verbose_name="Дата обновления")

    class Meta:
        UniqueConstraint(fields=['user','node'],name='unique_user_node')




