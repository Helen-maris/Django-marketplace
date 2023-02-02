# Generated by Django 3.2.9 on 2022-02-01 21:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0020_subscription'),
    ]

    operations = [
        migrations.CreateModel(
            name='SMSLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.IntegerField(max_length=4)),
                ('confirmed', models.BooleanField()),
                ('response', models.CharField(max_length=50)),
                ('seller', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main.seller')),
            ],
        ),
    ]
