from django.db import models

# Create your models here.


class TestData(models.Model):
    name = models.CharField(blank=True, max_length=255)
    address = models.CharField(blank=True, max_length=255)

    def __str__(self):
        return self.name
