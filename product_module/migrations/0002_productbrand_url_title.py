# Generated by Django 4.2.3 on 2023-08-13 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_module', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='productbrand',
            name='url_title',
            field=models.CharField(db_index=True, default='url_title', max_length=300, verbose_name='عنوان url'),
            preserve_default=False,
        ),
    ]
