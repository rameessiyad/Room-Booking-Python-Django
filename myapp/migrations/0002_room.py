# Generated by Django 5.0.4 on 2024-04-13 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rno', models.IntegerField()),
                ('rt', models.CharField(max_length=40)),
            ],
        ),
    ]
