from django.db import models

# Create your models here.
class Result(models.Model):
    #created_on = models.DateTimeField(auto_now=True, auto_created=True)
    data_json = models.TextField(null=True)
    finished = models.BooleanField(default=False)
    args = models.TextField(null=True)