from django.urls import path

from .views import ListMovies, ImportDataset, MovieDetails

app_name = 'backend'

urlpatterns = [
    path('movies/', ListMovies.as_view()),
    path('db/', ImportDataset.as_view()),
    path('movies/<int:movieId>/', MovieDetails.as_view()),
]
