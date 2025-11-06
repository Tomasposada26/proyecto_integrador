import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Acentos.settings')
django.setup()
from books.models import Book

book = Book.objects.filter(title__icontains='lorax').first()
if book:
    print(f"The Lorax tiene {book.num_pages or 'un número de páginas no especificado'} páginas.")
else:
    print("No se encontró el libro 'The Lorax'.")
