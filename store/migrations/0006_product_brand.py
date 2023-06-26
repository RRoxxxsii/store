# Generated by Django 4.2.2 on 2023-06-18 07:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_brand_alter_category_category_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='brand',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='store.brand', verbose_name='Бренд'),
            preserve_default=False,
        ),
    ]