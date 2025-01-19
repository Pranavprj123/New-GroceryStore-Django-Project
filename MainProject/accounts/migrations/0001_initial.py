# Generated by Django 5.1.2 on 2025-01-17 14:56

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('locality', models.CharField(max_length=200)),
                ('city', models.CharField(max_length=50)),
                ('zipcode', models.CharField(max_length=10)),
                ('state', models.CharField(choices=[('Maharashtra', 'Maharashtra'), ('Gujarat', 'Gujarat'), ('Rajasthan', 'Rajasthan'), ('Karnataka', 'Karnataka'), ('Tamil Nadu', 'Tamil Nadu'), ('Kerala', 'Kerala'), ('Uttar Pradesh', 'Uttar Pradesh'), ('Madhya Pradesh', 'Madhya Pradesh'), ('West Bengal', 'West Bengal'), ('Bihar', 'Bihar'), ('Punjab', 'Punjab'), ('Haryana', 'Haryana'), ('Andhra Pradesh', 'Andhra Pradesh'), ('Telangana', 'Telangana'), ('Odisha', 'Odisha'), ('Assam', 'Assam'), ('Chhattisgarh', 'Chhattisgarh'), ('Jharkhand', 'Jharkhand'), ('Himachal Pradesh', 'Himachal Pradesh'), ('Uttarakhand', 'Uttarakhand')], max_length=50)),
                ('address', models.CharField(max_length=255, null=True)),
                ('country', models.CharField(max_length=50, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True)),
                ('region', models.CharField(blank=True, max_length=50, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Customer',
                'verbose_name_plural': 'Customers',
            },
        ),
    ]
