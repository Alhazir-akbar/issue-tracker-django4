from django.db import models
from django.contrib.auth.models import User
from bug.models import Ticket


class UserProfile(models.Model):
    USER_ROLES = [
        ('reporting', 'Reporting'),
        ('support', 'Support'),
        ('developer', 'Developer'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=USER_ROLES, verbose_name="Peran", default="reporting")
    supported_reports = models.ManyToManyField('bug.Ticket', blank=True, related_name='supporters', verbose_name="Laporan yang didukung")


    def __str__(self):
        return self.user.username
