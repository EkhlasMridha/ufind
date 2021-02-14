from django.db import models

# Create your models here.


class MissingPerson(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=250)
    location = models.CharField(max_length=200)
    image = models.ImageField(upload_to="images/")

    def __str__(self):
        return "{}".format(self.name)
