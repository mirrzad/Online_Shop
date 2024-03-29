# Generated by Django 4.2.3 on 2023-08-14 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_module', '0003_slider'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteBanner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='عنوان')),
                ('url', models.URLField(blank=True, max_length=400, null=True, verbose_name='آدرس')),
                ('is_active', models.BooleanField(verbose_name='فعال/غیرفعال')),
                ('image', models.ImageField(upload_to='images/banner', verbose_name='عکس بنر')),
                ('position', models.CharField(choices=[('product_list', 'صفحه لیست محصولات'), ('product_detail', 'صفحه جزئیات محصولات'), ('about_us', 'درباره ما')], max_length=100, verbose_name='جایگاه نمایش')),
            ],
            options={
                'verbose_name': '',
                'verbose_name_plural': '',
            },
        ),
    ]
