from django.db import models

from django.db.models import Avg

'''
Managers
'''

class LinksManager(models.Manager):
    def movie_id(self, id):
        imdb_id = self.filter(movie_id=id).values('imdb_id')[0]['imdb_id']
        return 'https://www.imdb.com/title/tt0' + str(imdb_id)

class MoviesManager(models.Manager):
    def id(self, id):
        return self.filter(movie_id=id)
    def title_by_id(self, id):
        return self.filter(movie_id=id).values('title')[0]['title']
    def year_by_id(self, id):
        return self.filter(movie_id=id).values('year')[0]['year']
    def genres_by_id(self, id):
        genres = self.filter(movie_id=id).values('genres')[0]['genres']
        genres = genres.split('|')
        return genres
    def by_year(self, m_year):
        return self.filter(year=m_year)
    def by_tags(self, tags):
        movie_ids = []
        for tag in tags:
            movies = Tags.objects.filter(tag=tag).values('movie_id')
            for m_id in range(0, len(movies)-1):
                movie_ids.append(int(movies[m_id]['movie_id']))
        return self.filter(movie_id__in=movie_ids)

class RatingsManager(models.Manager):
    def movie_id(self, id):
        return self.filter(movie_id=id)

    def movie_avg(self, id):
        avg_score = self.filter(movie_id=id).aggregate(Avg('rating'))['rating__avg']
        avg_score = round(avg_score, 1)
        return avg_score

class TagsManager(models.Manager):
    def movie_id(self, id):
        tags = self.filter(movie_id=id).values('tag')
        tags_string = ''
        for tag in range(0, len(tags) - 1):
            tags_string += tags[tag]['tag'] + ' '
        return tags_string

'''
Models
'''

class Links(models.Model):
    movie_id = models.IntegerField(blank=True, default=0)
    imdb_id =  models.IntegerField(blank=True, default=0)
    tmdb_id = models.IntegerField(blank=True, default=0)

    class Meta:
        ordering = ('movie_id',)

    objects = LinksManager()

class Movies(models.Model):
    movie_id = models.IntegerField(default=0)
    title = models.CharField(max_length=256, blank=True, default='')
    year = models.TextField(max_length=16, blank=True, default='')
    genres = models.TextField(max_length=256, blank=True, default='')

    objects =  MoviesManager()

    class Meta:
        ordering = ('movie_id',)

    def save(self, *args, **kwargs):
        if '(' in self.title:
            self.year = self.title.rsplit('(',1)[1].replace(')', '')
        else:
            self.year = 0

        self.title = self.title.rsplit('(',1)[0]
        super(Movies, self).save(*args, **kwargs)

class Ratings(models.Model):
    user_id = models.IntegerField(default=0)
    movie_id = models.IntegerField(default=0)
    rating = models.DecimalField(max_digits=8, decimal_places=1, default=0)
    timestamp = models.IntegerField(default=0)

    class Meta:
        ordering = ('movie_id',)

    objects =  RatingsManager()

class Tags(models.Model):
    user_id = models.IntegerField(default=0)
    movie_id = models.IntegerField(default=0)
    tag = models.TextField(max_length=256, blank=True, default='')
    timestamp = models.IntegerField(default=0)

    class Meta:
        ordering = ('movie_id',)

    objects =  TagsManager()
