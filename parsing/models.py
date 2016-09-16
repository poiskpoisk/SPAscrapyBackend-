from django.db import models

# Create your models here.

class StatMsg(models.Model):
    parsingURL = models.CharField(max_length=200, blank=True, default='')
    msg = models.CharField(max_length=200, blank=True, default='')

    def __str__(self):
        return '%s %s' % (self.parsingURL, self.msg)

class QueneURLs(models.Model):
    parsingURL = models.CharField(max_length=200, blank=True, default='')

    def __str__(self):
        return '%s' % (self.parsingURL)

class ParsingData(models.Model):
    parsingURL = models.CharField(max_length=200,blank=True, default='')
    title = models.CharField(max_length=200, blank=True, default='')
    h1 = models.CharField(max_length=200, blank=True, default='')
    source_image_url = models.CharField(max_length=200, blank=True, default='')
    image_url = models.CharField(max_length=200, blank=True, default='')


class ScheduleQuene(models.Model):
    strDataTime = models.CharField(max_length=100, default='')



