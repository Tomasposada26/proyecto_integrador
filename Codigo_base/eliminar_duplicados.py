# Script para eliminar libros duplicados por título en Django
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Acentos.settings')
django.setup()

from books.models import Book
from collections import defaultdict

def eliminar_duplicados_por_titulo():
    titulos = defaultdict(list)
    for libro in Book.objects.all():
        titulos[libro.title.strip().lower()].append(libro)
    eliminados = 0
    for lista in titulos.values():
        if len(lista) > 1:
            # Mantener solo el primero, eliminar el resto
            for libro in lista[1:]:
                libro.delete()
                eliminados += 1
    print(f"Libros duplicados eliminados: {eliminados}")

if __name__ == "__main__":
    eliminar_duplicados_por_titulo()
