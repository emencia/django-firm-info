# Generated by Django 4.0.10 on 2023-05-22 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firm_info', '0002_alter_firmcontact_options_alter_firmcontact_address_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='firmcontact',
            name='baseline',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AddField(
            model_name='firmcontact',
            name='short_description',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='link',
            name='name',
            field=models.CharField(choices=[('linkedin', 'linkedin'), ('facebook', 'facebook'), ('twitter', 'twitter'), ('youtube', 'youtube'), ('instagram', 'instagram'), ('glassdoor', 'glassdoor'), ('bitbucket', 'bitbucket'), ('github', 'github'), ('gitlab', 'gitlab'), ('tiktok', 'tiktok'), ('twitch', 'twitch'), ('discord', 'discord'), ('vk', 'vk'), ('slack', 'slack'), ('whatsapp', 'whatsapp'), ('weechat', 'weechat')], max_length=255),
        ),
    ]
