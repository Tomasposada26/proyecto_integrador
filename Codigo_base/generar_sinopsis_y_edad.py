
import os
from dotenv import load_dotenv
load_dotenv()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Acentos.settings')
import django
django.setup()
import google.generativeai as genai
from books.models import Book

GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
genai.configure(api_key=GEMINI_API_KEY)

# Asignar rango de edad según género o título (simple ejemplo)
def sugerir_rango_edad(book):
    infantil = ['niño', 'niña', 'infantil', 'cuento', 'fábula', 'aventura']
    juvenil = ['juvenil', 'adolescente', 'joven', 'fantasía', 'aventura']
    if any(word in (book.genre or '').lower() or word in (book.title or '').lower() for word in infantil):
        return 'Infantil'
    if any(word in (book.genre or '').lower() or word in (book.title or '').lower() for word in juvenil):
        return 'Juvenil'
    return 'Adulto'

def generar_sinopsis(titulo):
    prompt = f"Dame una sinopsis breve y una recomendación para el libro titulado '{titulo}'. Responde en español."
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)
    return response.text.strip()

def actualizar_libros():
    libros = Book.objects.all()
    for libro in libros:
        actualizado = False
        if not libro.description:
            try:
                libro.description = generar_sinopsis(libro.title)
                actualizado = True
            except Exception as e:
                print(f"Error generando sinopsis para {libro.title}: {e}")
        if not libro.dominant_age_group:
            libro.dominant_age_group = sugerir_rango_edad(libro)
            actualizado = True
        if actualizado:
            libro.save()
            print(f"Actualizado: {libro.title}")

if __name__ == "__main__":
    actualizar_libros()
