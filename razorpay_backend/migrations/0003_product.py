# Generated by Django 5.0.8 on 2024-08-07 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('razorpay_backend', '0002_alter_transaction_signature'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
    ]
