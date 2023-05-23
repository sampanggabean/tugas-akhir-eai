from django.db import models

# Create your models here.
class Job(models.Model):
    position = models.TextField() 
    created_at = models.TextField() 
    location = models.TextField() 
    company = models.TextField() 
    source = models.TextField() 
    url = models.TextField()