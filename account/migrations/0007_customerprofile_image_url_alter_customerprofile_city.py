# Generated by Django 4.2.2 on 2023-06-10 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_alter_customerprofile_city'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerprofile',
            name='image_url',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/%Y/%m/%d/'),
        ),
        migrations.AlterField(
            model_name='customerprofile',
            name='city',
            field=models.CharField(default=None, max_length=250),
        ),
    ]