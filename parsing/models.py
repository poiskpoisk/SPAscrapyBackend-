from django.db import models

# Create your models here.

class StatMsg(models.Model):
    parsingURL = models.CharField(max_length=100, blank=True, default='')
    msg = models.CharField(max_length=100, blank=True, default='')

    def __str__(self):
        return '%s %s' % (self.parsingURL, self.msg)

class QueneURLs(models.Model):
    parsingURL = models.CharField(max_length=100, blank=True, default='')

    def __str__(self):
        return '%s' % (self.parsingURL)

