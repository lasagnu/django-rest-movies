# django-rest-movies

Simple rest-api application made for recruitment contest.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine.

### Prerequisites

```
Python 3.3+, Django 2.1+ and Postgres DB installed.
```

### Installing

Clone repository

```
git clone https://github.com/lasagnu/django-rest-movies.git && cd django-rest-movies
```

Initialize venv and install the dependencies

```
virtualenv venv && pip install -r requirements.txt
```

Edit settings file and fill the DB credentials and secret

```
./config/settings.py
```

Migrate the DB:

```
python manage.py makemigrations && python manage.py migrate
```

Finally run the server, i.e on port 3000:

```
python manage.py runserver 0.0.0.0:3000
```

If it is your first start, you have to initiate the DB, by sending POST request on /db endpoint with body:

```
{"source": "ml-latest-small"}
```

# Endpoints

/movie/ - lists all movies
/movie/<id> - lists movie details, where id = movie_id
/movies/?year=<int:year> - list of movies made in given year
/movies/?sort=<str:key> - sorted list of movies, ordered by key

/db with body {"source": "ml-latest-small"} - deletes current DB records and imports new data set

## Built With

* [Django](https://www.djangoproject.com/) - The web framework used


## Authors

* **Marek M** - [Lasagnu](https://github.com/Lasagnu)

## License

This project is licensed under the GPL3.0 License - see the [LICENSE.md](LICENSE.md) file for details
