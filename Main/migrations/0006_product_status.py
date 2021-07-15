# Generated by Django 3.2.5 on 2021-07-14 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0005_auto_20210714_1617'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='Status',
            field=models.IntegerField(choices=[(0, '正常浏览'), (1, '商家下架'), (2, '违规下架')], default=0, verbose_name='商品可浏览性'),
        ),
    ]