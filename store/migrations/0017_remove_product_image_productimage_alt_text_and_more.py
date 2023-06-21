# Generated by Django 4.2.2 on 2023-06-19 08:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0016_rename_image_url_productimage_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='image',
        ),
        migrations.AddField(
            model_name='productimage',
            name='alt_text',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Альтернативый текст'),
        ),
        migrations.AddField(
            model_name='productimage',
            name='is_feature',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='productimage',
            name='product',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='product_image', to='store.product'),
        ),
        migrations.AlterField(
            model_name='brand',
            name='brand_name',
            field=models.CharField(max_length=255, unique=True, verbose_name='Бренд'),
        ),
        migrations.AlterField(
            model_name='productimage',
            name='image',
            field=models.ImageField(default='media/images.png', upload_to='', verbose_name='Изображение'),
        ),
    ]
