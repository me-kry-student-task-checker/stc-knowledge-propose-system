from django.db import models


class Calculation(models.Model):
    numberA = models.FloatField
    numberB = models.FloatField
    operation = models.CharField(max_length=15)
    result = models.FloatField

