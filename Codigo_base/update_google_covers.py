
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Acentos.settings')
django.setup()

import requests
from books.models import Book

def get_google_books_cover(isbn):
    url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}"
    response = requests.get(url)
    data = response.json()
    try:
        image_url = data['items'][0]['volumeInfo']['imageLinks']['thumbnail']
        return image_url
    except (KeyError, IndexError):
        return None

def update_books_with_google_covers():
    books = Book.objects.filter(image_url__isnull=True).exclude(isbn='')
    for book in books:
        cover = get_google_books_cover(book.isbn)
        if cover:
            book.image_url = cover
            book.save()
            print(f"Actualizada portada para: {book.title}")
        else:
            print(f"No se encontró portada para: {book.title}")

if __name__ == "__main__":
    update_books_with_google_covers()
