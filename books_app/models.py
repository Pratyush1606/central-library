from django.db import models

class Book(models.Model):
    book_id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=100)
    published = models.IntegerField()
    author = models.CharField(max_length=100)
    domain = models.CharField(max_length=200)
    is_available = models.BooleanField(default=False)
