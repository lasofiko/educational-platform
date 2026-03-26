from django.db import models

# Create your models here.


class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название предмета")
    description = models.TextField(blank=True, verbose_name="Описание")
    icon = models.CharField(max_length=50, blank=True, verbose_name="Иконка")

    class Meta:
        verbose_name = "Предмет"
        verbose_name_plural = "Предметы"
        ordering = ["name"]

    def __str__(self):
        return self.name