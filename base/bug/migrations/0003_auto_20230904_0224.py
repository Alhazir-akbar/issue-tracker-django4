# Generated by Django 2.2 on 2023-09-04 02:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bug', '0002_ticket_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='file',
            field=models.FileField(upload_to='attachments/', verbose_name='Upload File Pendukung'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]