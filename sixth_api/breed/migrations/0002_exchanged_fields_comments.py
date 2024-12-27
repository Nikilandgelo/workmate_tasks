# Generated by Django 5.1.4 on 2024-12-24 09:39

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('breed', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='breed',
            name='exercise_needs',
            field=models.PositiveSmallIntegerField(db_comment='Exercise needs from 1 to 5', help_text='Breed exercise needs must be between 1 and 5.', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name='Exercise Needs'),
        ),
        migrations.AlterField(
            model_name='breed',
            name='friendliness',
            field=models.PositiveSmallIntegerField(db_comment='Friendliness from 1 to 5', help_text='Breed friendliness must be between 1 and 5.', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name='Friendliness'),
        ),
        migrations.AlterField(
            model_name='breed',
            name='name',
            field=models.CharField(db_comment='Unique name of the breed with length of 255', help_text='Breed name must be unique.', max_length=255, unique=True, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='breed',
            name='shedding_amount',
            field=models.PositiveSmallIntegerField(db_comment='Shedding amount from 1 to 5', help_text='Breed shedding amount must be between 1 and 5.', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name='Shedding Amount'),
        ),
        migrations.AlterField(
            model_name='breed',
            name='size',
            field=models.CharField(choices=[('Tiny', 'Tiny'), ('Small', 'Small'), ('Medium', 'Medium'), ('Large', 'Large')], db_comment='Size of the breed which can be one of: Tiny, Small, Medium, or Large', help_text='Breed size must be one of: Tiny, Small, Medium, or Large.', max_length=6, verbose_name='Size'),
        ),
        migrations.AlterField(
            model_name='breed',
            name='trainability',
            field=models.PositiveSmallIntegerField(db_comment='Trainability from 1 to 5', help_text='Breed trainability must be between 1 and 5.', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name='Trainability'),
        ),
    ]
