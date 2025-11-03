
import os
import google.generativeai as genai
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
from dotenv import load_dotenv
load_dotenv()
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
genai.configure(api_key=GEMINI_API_KEY)

@csrf_exempt
@require_POST
def ia_book_synopsis(request):
    try:
        data = json.loads(request.body)
        book_title = data.get('book_title', '').strip()
        if not book_title:
            return JsonResponse({'error': 'No se proporcionó el título del libro.'}, status=400)
        # Prompt para la IA
        prompt = f"Dame una sinopsis breve y una recomendación para el libro titulado '{book_title}'. Responde en español."
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        text = response.text.strip()
        return JsonResponse({'result': text})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
