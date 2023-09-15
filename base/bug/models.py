from django.db import models
from django.contrib.auth.models import User

class Ticket(models.Model):
    PRIORITY_CHOICES = [
        ('Minor', 'Minor'),
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]
    title = models.CharField(max_length=255, verbose_name="Judul Laporan")
    description = models.TextField(verbose_name="Deskripsi Laporan")
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='Minor')
    reporting_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Pelapor")
    STATUS_CHOICES = [
        ('Proses', 'Terkirim Ke Support'),      # Dari reporting ke support
        ('ToDeveloper', 'Tiket Dari Support'),  # Dari Support ke devloper
        ('Selesai', 'Selesai'),                 # Dari Developer ke reporting
        ('ToSupport', 'Tiket Dari Developer'),  # Dari developer ke support

    ]
    status = models.CharField(max_length=55, choices=STATUS_CHOICES, default='Proses')
    reporter = models.CharField(max_length=255, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='attachments/', verbose_name="Upload File Pendukung", blank=True, null=True)
    def __str__(self):
        return self.title
    
    
class Comment(models.Model):
    ticket = models.ForeignKey('Ticket', on_delete=models.CASCADE, related_name='comments')
    parent_comment = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    # created_at = models.DateTimeField(auto_now_add=True)