# Generated by Django 4.2.4 on 2023-09-01 01:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bug', '0001_initial'),
        ('_profile', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='supported_reports',
            field=models.ManyToManyField(blank=True, related_name='supporters', to='bug.ticket', verbose_name='Laporan yang didukung'),
        ),
    ]
