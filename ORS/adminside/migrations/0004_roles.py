# Generated by Django 2.2.4 on 2020-03-21 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminside', '0003_auto_20200321_1443'),
    ]

    operations = [
        migrations.CreateModel(
            name='Roles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Rolename', models.CharField(max_length=50)),
                ('Permissions', models.CharField(max_length=300)),
            ],
        ),
    ]
