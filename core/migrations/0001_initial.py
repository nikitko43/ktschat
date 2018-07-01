# Generated by Django 2.0.6 on 2018-07-01 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=30)),
                ('text', models.TextField(null=True)),
                ('time', models.DateTimeField(auto_now=True)),
                ('attached_file', models.FileField(null=True, upload_to='')),
            ],
        ),
    ]
