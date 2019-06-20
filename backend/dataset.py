import requests
import os
import csv

from zipfile import ZipFile, BadZipFile, LargeZipFile
from pathlib import Path

from .models import Links, Movies, Ratings, Tags

from django.conf import settings

#cwd = Path(os.path.dirname(os.path.realpath(__file__)))
cwd = Path(settings.STATIC_DIR)
dataset_url = settings.DATASET_URL

data_path = cwd / "data.zip"
file_links = cwd / "ml-latest-small/links.csv"        # 'movieId', 'imdbId', 'tmdbId'
file_movies = cwd / "ml-latest-small/movies.csv"      # 'movieId', 'title', 'genres'
file_ratings = cwd / "ml-latest-small/ratings.csv"    # 'userId', 'movieId', 'rating', 'timestamp'
file_tags = cwd / "ml-latest-small/tags.csv"          # 'userId', 'movieId', 'tag', 'timestamp'

file_set = [ file_links, file_movies, file_ratings, file_tags ]

csv_file_validator = [
                        ['movieId', 'imdbId', 'tmdbId'],
                        ['movieId', 'title', 'genres'],
                        ['userId', 'movieId', 'rating', 'timestamp'],
                        ['userId', 'movieId', 'tag', 'timestamp']
                     ]

def f_int(val):
    try:
        fint = int(val)
        return fint
    except ValueError:
        return 0

def extract_zip(file_path):
    '''
    extract zip file at given path, return True on success
    '''
    try:
        with ZipFile(file_path, 'r') as zipObj:
            zipObj.extractall(path=cwd)
            print('File has been extracted: ',file_path)
            return True
    except BadZipFile as errbad:
        print('ZIP file is not valid:',errbad)
    except LargeZipFile as errbig:
        print('ZIP file is too big:',errbig)
    except:
        print('Zip file: ', file_path, ' encountered unknown error.')

def zip_is_valid(file_path):
    if extract_zip(file_path):
        try:
            for file in range(0,len(file_set)):
                with open(file_set[file], encoding="utf8") as csv_file:
                    csv_reader = csv.reader(csv_file, delimiter=',')
                    first_row = next(csv_reader)
                    for column in range(0, len(first_row)):
                        if not first_row[column] == csv_file_validator[file][column]:
                            return False
            return True
        except IOError as errio:
            print('I/O Error: ',errio)
        except:
            print('Unexpected error while reading the file.')

def save_file(file_path, req):
    '''
    save data from request to file at given target path, returns True on success
    '''
    try:
        with open(file_path, 'wb') as file:
            file.write(req.content)
            print('File has been saved in: ', file_path)
            return True
    except os.error as erros:
        print('File I/O Error:',erros)

def dataset_is_downloaded(url, dest_path):
    '''
    download file data via GET request and then save it,
    returns True if file is successfully downloaded and saved on the hard drive
    '''
    try:
        req = requests.get(url,timeout=3)
        req.raise_for_status()
        print('File data has been downloaded.')
        return save_file(dest_path, req)
    except requests.exceptions.HTTPError as errhttp:
        print ('Http Error:',errhttp)
    except requests.exceptions.ConnectionError as errcon:
        print ('Connection Error:',errcon)
    except requests.exceptions.Timeout as errtimeout:
        print ('Timeout Error:',errtimeout)
    except requests.exceptions.RequestException as err:
        print ('General Error:',err)

def delete_current_db():
    try:
        Links.objects.all().delete()
        Movies.objects.all().delete()
        Ratings.objects.all().delete()
        Tags.objects.all().delete()
    except:
        print('Error during DB cleanup.')


def import_dataset():
    if dataset_is_downloaded(dataset_url, data_path) and zip_is_valid(data_path):
        delete_current_db();
        with open(file_links) as links:
            reader = csv.DictReader(links)
            for row in reader:
                model = Links(
                                movie_id = f_int(row['movieId']), 
                                imdb_id = f_int(row['imdbId']), 
                                tmdb_id = f_int(row['tmdbId'])
                                )
                model.save()
        with open(file_movies) as movies:
            reader = csv.DictReader(movies)
            for row in reader:
                model = Movies(
                                movie_id = int(row['movieId']), 
                                title = row['title'], 
                                genres = row['genres']
                                )
                model.save()
        with open(file_ratings) as ratings:
            reader = csv.DictReader(ratings)
            for row in reader:
                model = Ratings(
                                user_id=row['userId'], 
                                movie_id=row['movieId'], 
                                rating=float(row['rating']), 
                                timestamp=row['timestamp']
                                )
                model.save()
        with open(file_tags) as tags:
            reader = csv.DictReader(tags)
            for row in reader:
                model = Tags(
                                user_id=row['userId'], 
                                movie_id=row['movieId'], 
                                tag=row['tag'], 
                                timestamp=row['timestamp']
                                )
                model.save()
