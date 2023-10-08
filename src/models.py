from django.db import models
from django.utils import timezone


class Meeting(models.Model):
    name = models.CharField(max_length=100, null=True, default=None)
    date = models.DateTimeField(null=True, default=None)
    origin = models.CharField(max_length=255, null=True, default=None)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.origin:
            self.origin = 'default_value_if_header_is_missing'
        super(Meeting, self).save(*args, **kwargs)


class OriginEmailStatus(models.Model):
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, null=True)
    
    email_sent = models.BooleanField(default=False)
    generatedLink = models.CharField(max_length=255, null=True, default=None)
    send_delay = models.IntegerField(default=2) 

    #    geeks_field = models.IntegerField() 
    email = models.EmailField(null=True, default=None)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.meeting.name} - {self.generatedLink}'
