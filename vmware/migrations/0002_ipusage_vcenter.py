# Generated by Django 2.1.7 on 2019-04-15 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('vmware', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='IpUsage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ipaddress', models.GenericIPAddressField()),
            ],
        ),
        migrations.CreateModel(
            name='Vcenter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=100)),
                ('pwd', models.CharField(max_length=100)),
                ('port', models.CharField(default=443, max_length=20)),
                ('host', models.GenericIPAddressField()),
            ],
        ),
    ]
