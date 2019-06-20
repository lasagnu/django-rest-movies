from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import FieldDoesNotExist


from .models import Links, Movies, Ratings, Tags
from .dataset import import_dataset

import os

cwd = os.path.dirname(os.path.realpath(__file__))

def query_set_to_dict(qsv):
    return [item for item in qsv]

class MovieDetails(APIView):
    def get(self, request, movieId):
        if Movies.objects.id(movieId).exists():
            return Response({
                'title': Movies.objects.title_by_id(movieId),
                'score': Ratings.objects.movie_avg(movieId),
                'genres': Movies.objects.genres_by_id(movieId), 
                'link': Links.objects.movie_id(movieId),
                'year': Movies.objects.year_by_id(movieId)
                }, status=status.HTTP_200_OK)
        else:
            return Response({'response':'Does not exist.'}, status=status.HTTP_404_NOT_FOUND)

class ListMovies(APIView):
    def get(self, request):
        if 'year' and 'sort' in request.query_params.keys():
            field_exists = None
            abs_sort = request.query_params['sort'].replace('-','')
            try:
                field_exists = Movies._meta.get_field(abs_sort)
            except FieldDoesNotExist as e:
                return Response({'response':str(e)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            
            if field_exists:
                movies = Movies.objects.by_year(request.query_params['year']).order_by(request.query_params['sort'])

        elif 'year' in request.query_params.keys():
            movies = Movies.objects.by_year(request.query_params['year'])
        elif 'sort' in request.query_params.keys():
            movies = Movies.objects.all().order_by(request.query_params['sort'])
        else:
            movies = Movies.objects.all()


        movies = movies.values('movie_id', 'year', 'title')
        movies_dict = query_set_to_dict(movies)

        if not movies_dict:
            return Response({'response':'No movies found for given criteria.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(movies_dict, status=status.HTTP_200_OK)

class ImportDataset(APIView):
    def post(self, request):
        if request.data['source'] == 'ml-latest-small':
            try:
                import_dataset()
                return Response({'response':'Import completed.'}, status=status.HTTP_200_OK)
            except Exception as e:
                print(e)
                return Response({'response':'Import failed.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'response':'Wrong parameters.'}, status=status.HTTP_400_BAD_REQUEST)
