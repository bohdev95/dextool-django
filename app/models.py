from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    pass

class Data(models.Model):
    timestamp = models.DateTimeField(null=True, blank=True)
    supply =  models.IntegerField(null=True, blank=True)
    category =  models.TextField(null=True, blank=True)
    number_of_addresses = models.IntegerField(null=True, blank=True)
    sum_of_balances = models.FloatField(null=True, blank=True)
    average_balance = models.FloatField(null=True, blank=True)
    percent_of_supply = models.FloatField(null=True, blank=True)
    project_id = models.IntegerField(null=True, blank=True)

class Projects(models.Model):
    name = models.TextField(null=True, blank=True)
    file_name = models.TextField(null=True, blank=True)
    download_url = models.TextField(null=True, blank=True)
    status = models.IntegerField(null=True, blank=True)