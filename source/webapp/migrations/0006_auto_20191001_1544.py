# Generated by Django 2.2.5 on 2019-10-01 09:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0005_auto_20190927_2058'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Category', 'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterModelOptions(
            name='comment',
            options={},
        ),
    ]
