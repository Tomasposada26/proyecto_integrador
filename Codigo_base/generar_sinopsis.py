import os
import django

# Configura el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Acentos.settings')
django.setup()

from books.models import Book

def generar_sinopsis_completa(book):
    autor = book.authors or "Autor desconocido"
    genero = book.genre or "género no especificado"
    anio = book.publication_date or "año desconocido"
    titulo = book.title or "Obra sin título"
    rating = f"{book.average_rating:.2f}" if book.average_rating else "sin calificación"
    sinopsis = (
        f"\nTítulo: {titulo}\n"
        f"Autor: {autor}\n"
        f"Género: {genero}\n"
        f"Año de publicación: {anio}\n"
        f"Calificación promedio: {rating}\n\n"
        f"Sinopsis: '{titulo}' es una obra destacada dentro del género {genero}, escrita por {autor} y publicada en {anio}. "
        f"Este libro invita al lector a sumergirse en una narrativa única, explorando temas relevantes y universales. "
        f"La pluma de {autor} logra transmitir emociones profundas y reflexiones sobre la condición humana, "
        f"ofreciendo una experiencia literaria enriquecedora.\n\n"
        f"A lo largo de sus páginas, '{titulo}' desarrolla personajes memorables y situaciones que invitan a la empatía y el análisis crítico. "
        f"Recomendado tanto para quienes buscan entretenimiento como para quienes desean ampliar su perspectiva sobre el mundo. "
        f"Esta obra ha sido valorada por los lectores con una calificación promedio de {rating}, consolidándose como una referencia dentro de su género."
    )
    return sinopsis

count = 0
for book in Book.objects.all():
    sinopsis = generar_sinopsis_completa(book)
    book.description = sinopsis
    book.save()
    count += 1
    print(f"Sinopsis generada para: {book.title}")

print(f"¡Sinopsis generadas para {count} libros!")
