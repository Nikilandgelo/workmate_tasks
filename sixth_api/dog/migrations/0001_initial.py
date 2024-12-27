# Generated by Django 5.1.4 on 2024-12-24 08:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('breed', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_comment='Name of the dog', max_length=255)),
                ('age', models.PositiveSmallIntegerField(db_comment='Age of the dog')),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], db_comment='Gender of the dog', max_length=6)),
                ('color', models.CharField(db_comment='Color of the dog', max_length=100)),
                ('favorite_food', models.CharField(db_comment='Favorite food of the dog', max_length=255)),
                ('favorite_toy', models.CharField(db_comment='Favorite toy of the dog', max_length=255)),
                ('breed', models.ForeignKey(db_comment='Breed of the dog', on_delete=django.db.models.deletion.CASCADE, related_name='dogs', to='breed.breed')),
            ],
        ),
    ]
