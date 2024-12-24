# Generated by Django 5.1.4 on 2024-12-24 08:51

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Breed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_comment='Name of the breed', max_length=255, unique=True)),
                ('size', models.CharField(choices=[('Tiny', 'Tiny'), ('Small', 'Small'), ('Medium', 'Medium'), ('Large', 'Large')], db_comment='Size of the breed', max_length=6)),
                ('friendliness', models.PositiveSmallIntegerField(db_comment='Friendliness of the breed', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('trainability', models.PositiveSmallIntegerField(db_comment='Trainability of the breed', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('shedding_amount', models.PositiveSmallIntegerField(db_comment='Shedding amount of the breed', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('exercise_needs', models.PositiveSmallIntegerField(db_comment='Exercise needs of the breed', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
            ],
        ),
    ]
