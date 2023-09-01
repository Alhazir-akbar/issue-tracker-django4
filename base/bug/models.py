from django.db import models
from django.contrib.auth.models import User

class Ticket(models.Model):
    PRIORITY_CHOICES = [
        ('Minor', 'Minor'),
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]
    title = models.CharField(max_length=255)
    description = models.TextField()
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='Medium')
    reporting_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Pelapor")
    STATUS_CHOICES = [
        ('Proses', 'Proses'),
        ('Diteruskan ke Pengembang', 'Diteruskan ke Pengembang'),
        ('Selesai', 'Selesai'),
        ('Kembalikan ke Support', 'Kembalikan Ke Support'),
        # Tambahkan status lain sesuai kebutuhan
    ]
    status = models.CharField(max_length=55, choices=STATUS_CHOICES, default='Proses')
    position = models.CharField(max_length=20, blank=True, null=True)
    attachment = models.ForeignKey('Attachment', on_delete=models.CASCADE, blank=True, null=True, related_name='ticket_attachments')  
    reporter = models.CharField(max_length=255, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title
    
class Attachment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='attachments')  
    file = models.FileField(upload_to='attachments/')

class Comment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='comments')  
    message = models.TextField()
    creator = models.CharField(max_length=255)