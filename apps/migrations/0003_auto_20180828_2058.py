# Generated by Django 2.1 on 2018-08-28 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0002_bigtestinfotable_wdjid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='celltesthistorydatatable',
            name='tCO2',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='CO2数据修改时间'),
        ),
    ]
