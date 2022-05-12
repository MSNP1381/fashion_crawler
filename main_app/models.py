from django.db import models


# Create your models here.
class Media(models.Model):
    title = models.CharField(max_length=400)
    images = models.JSONField()
    description = models.TextField(blank=True)
    price = models.CharField(max_length=40)
    datetime = models.DateTimeField(auto_now=True)
    url = models.URLField()
