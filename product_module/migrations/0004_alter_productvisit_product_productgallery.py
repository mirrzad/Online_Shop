# Generated by Django 4.2.3 on 2023-08-19 07:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product_module', '0003_productvisit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productvisit',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='visits', to='product_module.product', verbose_name='بازدید محصول'),
        ),
        migrations.CreateModel(
            name='ProductGallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/product_gallery')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='galleries', to='product_module.product', verbose_name='محصول')),
            ],
            options={
                'verbose_name': 'گالری محصول',
                'verbose_name_plural': 'گالری محصولات',
            },
        ),
    ]