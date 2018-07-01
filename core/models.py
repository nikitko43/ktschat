from django.db import models

# Create your models here.

class Message(models.Model):
    author = models.CharField(max_length=30)
    text = models.TextField(blank=True, null=True, default='')
    time = models.DateTimeField(auto_now=True)
    attached_file = models.FileField(blank=True, null=True, default=None)

    def __str__(self):
        return self.text
