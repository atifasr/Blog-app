# Generated by Django 3.0.6 on 2020-05-25 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('practice', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='blog_det',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blog_name', models.CharField(max_length=200)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('text', models.TextField()),
            ],
        ),
    ]
