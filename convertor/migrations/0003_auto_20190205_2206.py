# Generated by Django 2.1.5 on 2019-02-05 22:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('convertor', '0002_currencies_exchange_rate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currencies',
            name='currency_code',
            field=models.CharField(max_length=3, unique=True),
        ),
        migrations.AlterField(
            model_name='currencies',
            name='exchange_rate',
            field=models.DecimalField(decimal_places=2, max_digits=19),
        ),
    ]