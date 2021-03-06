# Generated by Django 3.0.5 on 2020-12-02 21:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0002_remove_tracking_user_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=200)),
                ('shipping_address', models.CharField(max_length=500)),
                ('state', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=500)),
                ('price', models.FloatField()),
            ],
        ),
        migrations.AddField(
            model_name='tracking',
            name='quantity',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
