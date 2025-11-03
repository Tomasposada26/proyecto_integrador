import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Acentos.settings')
django.setup()

from books.models import Book

def asignar_precios():
    libros = Book.objects.all()
    for libro in libros:
        # Asignar un precio aleatorio entre 25.000 y 120.000 COP
        libro.precio_cop = random.randint(25000, 120000)
        libro.save()
        print(f"{libro.title}: ${libro.precio_cop:,.0f} COP")

if __name__ == "__main__":
    asignar_precios()
