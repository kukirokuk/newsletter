from django.db import models
from datetime import datetime 

# Create your models here.
class Poll(models.Model):
	question = models.CharField(max_length=200, blank=True, null=True)
	pubdate = models.DateTimeField(auto_now_add=True, auto_now=False)
	bubdate = models.DateTimeField(default=datetime.now, blank=True)