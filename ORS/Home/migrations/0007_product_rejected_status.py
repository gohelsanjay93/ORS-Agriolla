# Generated by Django 2.2.4 on 2020-01-11 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0006_auto_20200109_1739'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='rejected_status',
            field=models.CharField(choices=[('yes', 'yes'), ('no', 'no')], default='no', max_length=5),
        ),
    ]
