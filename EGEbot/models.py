from django.db import models


class Photo(models.Model):
    file = models.ImageField()
    file_id = models.CharField(max_length=128, blank=True, default='')


class Task(models.Model):
    number = models.SmallIntegerField()
    text = models.TextField()
    answer = models.CharField(max_length=64)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, null=True, blank=True)


class User(models.Model):
    telegram_id = models.IntegerField(default=1, primary_key=True)
    current_task = models.ForeignKey(Task, on_delete=models.PROTECT, null=True, blank=True)
    state = models.SmallIntegerField(default=-1)
