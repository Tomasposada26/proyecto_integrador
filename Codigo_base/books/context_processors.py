from .models import Book
from django.urls import reverse

def common_context(request):
    genres = Book.objects.values_list('genre', flat=True).distinct().order_by('genre')
    authors = Book.objects.values_list('authors', flat=True).distinct().order_by('authors')
    featured_books = Book.objects.all()[:12]

    from .models import Favorite
    user_favorite_ids = []
    if request.user.is_authenticated:
        user_favorite_ids = list(Favorite.objects.filter(user=request.user).values_list('book_id', flat=True))
    return {
        'app_name': "Bookverse",
        'all_genres': genres,
        'all_authors': authors,
        'featured_books': featured_books,
        'user_favorite_ids': user_favorite_ids,
    }

def cart_counter(request):
    cart = request.session.get('cart', {})
    try:
        return {"cart_count": sum(int(q) for q in cart.values())}
    except Exception:
        return {"cart_count": 0}


def back_button_context(request):
    """Muestra el botón de volver atrás en todas las páginas menos el home."""
    current_path = request.path.rstrip('/')
    home_path = reverse("home").rstrip('/')
    return {
        "show_back_button": current_path != home_path and current_path != ""
    }
