import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Acentos.settings')
django.setup()

from books.models import Book

for book in Book.objects.all():
    if not hasattr(book, 'num_pages') or not getattr(book, 'num_pages', None):
        book.num_pages = random.randint(280, 435)
        book.save()
print('Páginas asignadas aleatoriamente a los libros.')
