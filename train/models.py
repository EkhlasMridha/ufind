from django.db import models

# Create your models here.


class FoundPerson(models.Model):
    description = models.CharField(max_length=300)
    phone = models.CharField(max_length=30)
    image = models.ImageField(upload_to="found/")
    location = models.CharField(max_length=300, default='unknown')

    def __str__(self):
        return "{}".format(self.description)
