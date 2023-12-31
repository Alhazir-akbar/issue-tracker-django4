# Generated by Django 4.2.4 on 2023-09-01 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bug', '0004_alter_ticket_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='position',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='reporter',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='status',
            field=models.CharField(choices=[('Proses', 'Proses'), ('Diteruskan ke Pengembang', 'Diteruskan ke Pengembang'), ('Selesai', 'Selesai'), ('Kembalikan ke Support', 'Kembalikan Ke Support')], default='Proses', max_length=55),
        ),
    ]
