# Configuración de Django para scripts standalone
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Acentos.settings')
django.setup()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Acentos.settings')
django.setup()


import requests
from books.models import Book
from dotenv import load_dotenv

load_dotenv()

# Asignar rango de edad según género o título (simple ejemplo)
def sugerir_rango_edad(book):
    infantil = ['niño', 'niña', 'infantil', 'cuento', 'fábula', 'aventura']
    juvenil = ['juvenil', 'adolescente', 'joven', 'fantasía', 'aventura']
    if any(word in (book.genre or '').lower() or word in (book.title or '').lower() for word in infantil):
        return 'Infantil'
    if any(word in (book.genre or '').lower() or word in (book.title or '').lower() for word in juvenil):
        return 'Juvenil'
    return 'Adulto'





# Detectar idioma y traducir si es necesario
def traducir_a_espanol(texto):
    try:
        # Detectar idioma
        detect_resp = requests.post(
            "https://libretranslate.de/detect",
            data={"q": texto}
        )
        idioma = detect_resp.json()[0]["language"]
        if idioma == "es":
            return texto
        # Traducir si no es español
        trad_resp = requests.post(
            "https://libretranslate.de/translate",
            data={"q": texto, "source": idioma, "target": "es"}
        )
        return trad_resp.json()["translatedText"]
    except Exception as e:
        print(f"Error traduciendo: {e}")
        return texto

def buscar_sinopsis_google_books(titulo, isbn=None):
    try:
        params = {"q": f"intitle:{titulo}", "maxResults": 1}
        if isbn:
            params["q"] = f"isbn:{isbn}"
        response = requests.get("https://www.googleapis.com/books/v1/volumes", params=params, timeout=15)
        if response.status_code == 200:
            data = response.json()
            if data.get("items"):
                volume = data["items"][0]
                desc = volume["volumeInfo"].get("description")
                if desc:
                    return traducir_a_espanol(desc.strip())
        return None
    except Exception as e:
        print(f"Error Google Books: {e}")
        return None

def generar_sinopsis_generica(titulo, genero=None):
    if genero:
        return f"'{titulo}' es un libro destacado dentro del género {genero}. Descubre una historia fascinante llena de emociones y sorpresas."
    else:
        return f"'{titulo}' es un libro fascinante que cautivará a cualquier lector."


def actualizar_libros():
    libros = Book.objects.all()
    for libro in libros:
        actualizado = False
        if not libro.description:
            sinopsis = None
            # Intenta buscar por ISBN si existe
            if hasattr(libro, 'isbn') and libro.isbn:
                sinopsis = buscar_sinopsis_google_books(libro.title, libro.isbn)
            # Si no hay sinopsis por ISBN, busca por título
            if not sinopsis:
                sinopsis = buscar_sinopsis_google_books(libro.title)
            # Si no hay sinopsis real, usa genérica
            if not sinopsis:
                sinopsis = generar_sinopsis_generica(libro.title, libro.genre)
            libro.description = sinopsis
            actualizado = True
        if not libro.dominant_age_group:
            libro.dominant_age_group = sugerir_rango_edad(libro)
            actualizado = True
        if actualizado:
            libro.save()
            print(f"Actualizado: {libro.title}")

if __name__ == "__main__":
    actualizar_libros()
