# Generated by Django 4.0.10 on 2023-06-02 15:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('firm_info', '0008_alter_tracking_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='socialsharing',
            options={'verbose_name': 'Social media share', 'verbose_name_plural': 'Social media shares'},
        ),
    ]