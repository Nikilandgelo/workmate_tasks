# Generated by Django 5.1.4 on 2024-12-24 09:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('breed', '0002_exchanged_fields_comments'),
        ('dog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dog',
            name='age',
            field=models.PositiveSmallIntegerField(db_comment='Age of the dog more or equal to 0', help_text='Dog age must be a positive integer.', verbose_name='Age'),
        ),
        migrations.AlterField(
            model_name='dog',
            name='breed',
            field=models.ForeignKey(db_comment="ID of the dog's breed", help_text='Dog breed must be a valid breed ID.', on_delete=django.db.models.deletion.CASCADE, related_name='dogs', to='breed.breed', verbose_name='Breed'),
        ),
        migrations.AlterField(
            model_name='dog',
            name='color',
            field=models.CharField(db_comment='Color of the dog with length of 100', help_text='Dog color must be a string with length of 100.', max_length=100, verbose_name='Color'),
        ),
        migrations.AlterField(
            model_name='dog',
            name='favorite_food',
            field=models.CharField(db_comment='Favorite food with length of 255', help_text='Dog favorite food must be a string with length of 255.', max_length=255, verbose_name='Favorite Food'),
        ),
        migrations.AlterField(
            model_name='dog',
            name='favorite_toy',
            field=models.CharField(db_comment='Favorite toy with length of 255', help_text='Dog favorite toy must be a string with length of 255.', max_length=255, verbose_name='Favorite Toy'),
        ),
        migrations.AlterField(
            model_name='dog',
            name='gender',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], db_comment='Gender which can be one of: Male or Female', help_text='Dog gender must be one of: Male, Female.', max_length=6, verbose_name='Gender'),
        ),
        migrations.AlterField(
            model_name='dog',
            name='name',
            field=models.CharField(db_comment='Name of the dog with length of 255', help_text='Dog name can be up to 255 characters long.', max_length=255, verbose_name='Name'),
        ),
    ]