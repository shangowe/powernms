# Generated by Django 2.2.4 on 2020-02-05 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Powerapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='module',
            name='id',
        ),
        migrations.AddField(
            model_name='module',
            name='port',
            field=models.CharField(max_length=4, null=True),
        ),
        migrations.AlterField(
            model_name='module',
            name='ipaddress',
            field=models.CharField(default='80080', max_length=200, primary_key=True, serialize=False),
            preserve_default=False,
        ),
    ]
