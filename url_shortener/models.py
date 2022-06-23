from django.db import models

# Create your models here.

class ShortUrl(models.Model):
    short_url = models.BigAutoField(primary_key=True)
    original_url = models.URLField(max_length=1024, unique=True)