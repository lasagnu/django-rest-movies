# Generated by Django 2.2.2 on 2019-06-20 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Links',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movie_id', models.IntegerField(default=0)),
                ('imdb_id', models.IntegerField(default=0)),
                ('tmdb_id', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ('movie_id',),
            },
        ),
        migrations.CreateModel(
            name='Movies',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movie_id', models.IntegerField(default=0)),
                ('title', models.CharField(blank=True, default='', max_length=128)),
                ('year', models.IntegerField(default=0)),
                ('genres', models.TextField(blank=True, default='', max_length=256)),
            ],
            options={
                'ordering': ('movie_id',),
            },
        ),
        migrations.CreateModel(
            name='Ratings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField(default=0)),
                ('movie_id', models.IntegerField(default=0)),
                ('rating', models.DecimalField(decimal_places=2, default=0, max_digits=2)),
                ('timestamp', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ('movie_id',),
            },
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField(default=0)),
                ('movie_id', models.IntegerField(default=0)),
                ('tag', models.TextField(blank=True, default='', max_length=128)),
                ('timestamp', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ('movie_id',),
            },
        ),
    ]