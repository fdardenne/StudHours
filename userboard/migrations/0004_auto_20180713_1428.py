# Generated by Django 2.0.7 on 2018-07-13 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userboard', '0003_auto_20180713_1420'),
    ]

    operations = [
        migrations.AlterField(
            model_name='work',
            name='extra_additional_hour_percent',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
        migrations.AlterField(
            model_name='work',
            name='extra_per_day',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
        migrations.AlterField(
            model_name='work',
            name='extra_public_holiday_percent',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
        migrations.AlterField(
            model_name='work',
            name='tax_percent',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
    ]
