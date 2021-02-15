from django.db import models
from user.models import User
# Create your models here.


class MissingPerson(models.Model):
    policeid = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=250)
    location = models.CharField(max_length=200)
    phone = models.CharField(max_length=30, default="No number")
    image = models.ImageField(upload_to="images/")
    isSolved = models.BooleanField(default=False)

    def __str__(self):
        return "{}".format(self.name)
