# Generated by Django 4.0.10 on 2023-05-17 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firm_info', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='firmcontact',
            options={'verbose_name': 'Compagny contact information', 'verbose_name_plural': 'Compagny contact information'},
        ),
        migrations.AlterField(
            model_name='firmcontact',
            name='address',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='firmcontact',
            name='city',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='firmcontact',
            name='country',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='firmcontact',
            name='email',
            field=models.EmailField(blank=True, default='', max_length=254),
        ),
        migrations.AlterField(
            model_name='firmcontact',
            name='phone_number',
            field=models.CharField(blank=True, default='', max_length=20),
        ),
        migrations.AlterField(
            model_name='firmcontact',
            name='postal_code',
            field=models.CharField(blank=True, default='', max_length=20),
        ),
    ]
