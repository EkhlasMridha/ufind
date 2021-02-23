from django.db import models
from user.models import User
# Create your models here.


class FoundPerson(models.Model):
    description = models.CharField(max_length=300)
    phone = models.CharField(max_length=30)
    image = models.ImageField(upload_to="found/")
    location = models.CharField(max_length=300, default='unknown')

    def __str__(self):
        return "{}".format(self.description)


class TrainingPerson(models.Model):
    policeid = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, default="unknown")
    description = models.CharField(max_length=300)
    phone = models.CharField(max_length=25)
    location = models.CharField(max_length=200)
    uploads = models.IntegerField(default=0, max_length=5)
    image = models.ImageField(upload_to="case/")
    isSolved = models.BooleanField(default=False)

    def __str__(self):
        return "{}".format(self.description)


class TrainingImage(models.Model):
    personId = models.ForeignKey(TrainingPerson, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="train/")

    def __str__(self):
        return "{}".format(self.personId)
