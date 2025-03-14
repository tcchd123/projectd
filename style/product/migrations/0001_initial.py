# Generated by Django 5.1.5 on 2025-02-14 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('specialize', models.CharField(max_length=500)),
                ('price', models.DecimalField(decimal_places=2, help_text='Price in INR (₹).', max_digits=12)),
                ('max_distance', models.FloatField(help_text='Maximum distance in km')),
                ('address', models.TextField()),
                ('contact', models.IntegerField()),
            ],
        ),
    ]
