from django.db import models


class Result(models.Model):
    URL = models.CharField(max_length=1024)
    created_on = models.DateTimeField(auto_now=True, auto_created=True)
    sis = models.FloatField()
    lcps = models.FloatField()
