# Generated by Django 5.1.3 on 2024-11-14 16:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0012_designrequests_done_status_image_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='designrequests',
            old_name='done_status_image',
            new_name='updated_image_sale',
        ),
    ]
