from rest_framework import serializers
from django.db import models

from .models import Movies

class MoviesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movies
        fields = ('movie_id', 'title', 'year', 'genres')


