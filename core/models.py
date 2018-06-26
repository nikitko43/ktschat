from django.db import models

# Create your models here.

class Message(models.Model):
    author = models.CharField(max_length=30)
    text = models.TextField()
    time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text
