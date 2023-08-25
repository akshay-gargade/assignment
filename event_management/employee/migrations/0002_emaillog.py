# Generated by Django 4.2.4 on 2023-08-25 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipient', models.EmailField(max_length=254)),
                ('subject', models.CharField(max_length=255)),
                ('status', models.CharField(max_length=10)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]