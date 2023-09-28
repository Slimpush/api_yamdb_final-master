import csv

from django.conf import settings
from django.core.management import BaseCommand

from users.models import User
from reviews.models import (Category, Comment, Genre,
                            GenreTitle, Review, Title)


FIELDS = {
    User: 'users.csv',
    Category: 'category.csv',
    Title: 'titles.csv',
    Genre: 'genre.csv',
    GenreTitle: 'genre_title.csv',
    Review: 'review.csv',
    Comment: 'comments.csv',
}


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        for model, data_csv in FIELDS.items():
            csv_path = f'{settings.BASE_DIR}/static/data/{data_csv}'
            with open(csv_path, 'r', encoding='utf-8',) as csv_file:
                reader = csv.DictReader(csv_file)
                model.objects.bulk_create(model(**data) for data in reader)
