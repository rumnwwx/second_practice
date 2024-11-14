# Generated by Django 5.1.3 on 2024-11-14 15:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0009_designrequests_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='comments',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='designrequests',
            name='category',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='catalog.category', verbose_name=''),
        ),
        migrations.AlterField(
            model_name='designrequests',
            name='status',
            field=models.CharField(choices=[('N', 'Новая'), ('P', 'Принято в работу'), ('C', 'Выполнено')], default='N', max_length=20),
        ),
    ]