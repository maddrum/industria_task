# Generated by Django 2.1.5 on 2019-02-05 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('convertor', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='currencies',
            name='exchange_rate',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]
