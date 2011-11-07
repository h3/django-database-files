from django.db import models
from database_files.manager import FileManager

class File(models.Model):
    name = models.CharField(max_length=255, unique=True)
    lastmod = models.DateTimeField(auto_now=True)
    content = models.TextField()
    size = models.IntegerField()
    
#   objects = FileManager()

