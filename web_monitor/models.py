from django.db import models


class Result(models.Model):
    ID = models.TextField(unique=True)
    created_on = models.DateTimeField(auto_now=True, auto_created=True)
    data_json = models.TextField(null=True)
    finished = models.BooleanField(default=False)
