import shelve
from django.shortcuts import get_object_or_404, render, redirect
from .recommendations import getRecommendations, transformPrefs, calculateSimilarItems, topMatches
from .populateDB import populate
from .progress import get_progress
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Book, Character, House, Rating
from whoosh.index import open_dir
from whoosh.qparser import MultifieldParser
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .forms import FavoriteForm, LikeForm, RemoveFavoriteForm, RemoveLikeForm

HOUSES_PER_PAGE = 24
CHARACTERS_PER_PAGE = 12


# Home
def home(request):
    book_list = Book.objects.filter(is_ice_and_fire=True).order_by('date')
    return render(request, 'home.html', {'books': book_list})


# Load data

@staff_member_required
@login_required
def populateDatabase(request):
    if not request.user.is_staff:
        return JsonResponse({'error': 'Superusers are not allowed to access this view.'}, status=403)

    houses = populate()  # Dictionary for RS {house_id:house_object}
    return render(request, 'load.html', {'message': 'Datos cargados con éxito', 'dict': houses})


@staff_member_required
@login_required
def get_load_progress(request):
    if not request.user.is_staff:
        return JsonResponse({'error': 'Superusers are not allowed to access this view.'}, status=403)

    progress = get_progress()
    print(progress)
    return JsonResponse(progress)


@staff_member_required
@login_required
def data(request):
    if not request.user.is_staff:
        return JsonResponse({'error': 'Superusers are not allowed to access this view.'}, status=403)

    return render(request, 'load.html')


# Find

def find(request):
    return render(request, 'find.html')


# Books

def books(request):
    book_list = Book.objects.all().order_by('date')
    return render(request, 'books.html', {'books': book_list})


# Characters

def characters(request):

    user = request.user
    Prefs = {}   # {userid: {itemid: rating}}
    shelf = shelve.open("dataRS.dat")
    ratings = Rating.objects.all()
    for ra in ratings:
        userid = int(ra.userId.id)
        itemid = int(ra.characterId.id)
        rating = int(ra.rating)
        Prefs.setdefault(userid, {})
        Prefs[userid][itemid] = rating
    shelf['Prefs'] = Prefs
    shelf.close()

    query = request.GET.get('q')
    selected_book = request.GET.get('books')
    selected_house = request.GET.get('house')
    character_list = Character.objects.all().order_by('name')
    if query or selected_book or selected_house:
        ix = open_dir("index2")
        with ix.searcher() as searcher:
            if query:
                myquery = MultifieldParser(
                    ["name", "text"], ix.schema
                ).parse(query)
                results = searcher.search(myquery)
                character_names = [str(hit['name']) for hit in results]
                character_list = Character.objects.filter(name__in=character_names)
            if selected_book:
                character_list = character_list.filter(books__title=selected_book).distinct()
            if selected_house:
                character_list = character_list.filter(house__name=selected_house).distinct()
        character_list = character_list.order_by('name')

    paginator = Paginator(character_list, CHARACTERS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if user.is_authenticated and user.id in Prefs:
        favourites = Character.objects.filter(
            id__in=Rating.objects.filter(userId=user, rating=2).values_list('characterId', flat=True)
        )
        liked_characters = Character.objects.filter(
            id__in=Rating.objects.filter(userId=user, rating=1).values_list('characterId', flat=True)
        )
    else:
        favourites = []
        liked_characters = []

    return render(request, 'characters.html', {
        'page_obj': page_obj,
        'query': query,
        'books': Book.objects.all().order_by('title'),
        'houses': House.objects.all().order_by('name'),
        'favourites': favourites, 'liked_characters': liked_characters
    })


def get_character_text_books_and_house(request):
    character_name = request.GET.get('name')
    ix = open_dir("index2")
    with ix.searcher() as searcher:
        myquery = MultifieldParser(["name"], ix.schema).parse(character_name)
        results = searcher.search(myquery)
        if results:
            character_text = results[0]['text']
            character_books = results[0]['books']
            character_house = results[0]['house']
        else:
            character_text = 'No disponible'
            character_books = 'No disponible'
            character_house = 'No disponible'
    return JsonResponse({'text': character_text, 'books': character_books, 'house': character_house})


@csrf_exempt
@require_POST
@login_required
def add_to_likes(request):
    form = LikeForm(request.POST)
    if form.is_valid():
        character_id = form.cleaned_data['character_id']
        character = get_object_or_404(Character, id=character_id)
        rating, created = Rating.objects.get_or_create(
            userId=request.user, characterId=character, defaults={'rating': 1}
        )
        if not created:
            rating.rating = 1
            rating.save()
    return redirect('characters')


@csrf_exempt
@require_POST
@login_required
def add_to_favorites(request):
    form = FavoriteForm(request.POST)
    if form.is_valid():
        character_id = form.cleaned_data['character_id']
        character = get_object_or_404(Character, id=character_id)
        rating, created = Rating.objects.get_or_create(
            userId=request.user, characterId=character, defaults={'rating': 2}
        )
        if not created:
            rating.rating = 2
            rating.save()
    return redirect('characters')


@csrf_exempt
@require_POST
@login_required
def remove_from_likes(request):
    form = RemoveLikeForm(request.POST)
    if form.is_valid():
        character_id = form.cleaned_data['character_id']
        character = get_object_or_404(Character, id=character_id)
        Rating.objects.filter(userId=request.user, characterId=character, rating=1).delete()
    return redirect('characters')


@csrf_exempt
@require_POST
@login_required
def remove_from_favorites(request):
    form = RemoveFavoriteForm(request.POST)
    if form.is_valid():
        character_id = form.cleaned_data['character_id']
        character = get_object_or_404(Character, id=character_id)
        rating = Rating.objects.filter(userId=request.user, characterId=character, rating=2).first()
        if rating:
            rating.rating = 1
            rating.save()
    return redirect('characters')


# Houses

def houses(request):
    query = request.GET.get('q')
    selected_book = request.GET.get('books')
    house_list = House.objects.all().order_by('name')
    if query or selected_book:
        ix = open_dir("index1")
        with ix.searcher() as searcher:
            if query:
                myquery = MultifieldParser(
                    ["name", "lord", "region", "place", "words", "founder"], ix.schema
                ).parse(query)
                results = searcher.search(myquery)
                house_names = [str(hit['name']) for hit in results]
                house_list = House.objects.filter(name__in=house_names).order_by('name')
            if selected_book:
                house_list = house_list.filter(books__title=selected_book).distinct().order_by('name')

    paginator = Paginator(house_list, HOUSES_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'houses.html', {
        'page_obj': page_obj,
        'query': query,
        'books': Book.objects.all().order_by('title')
    })


def get_house_text_and_books(request):
    house_name = request.GET.get('name')
    ix = open_dir("index1")
    with ix.searcher() as searcher:
        myquery = MultifieldParser(["name"], ix.schema).parse(house_name)
        results = searcher.search(myquery)
        if results:
            house_text = results[0]['text']
            house_books = results[0]['books']
        else:
            house_text = 'No disponible'
            house_books = 'No disponible'
    return JsonResponse({'text': house_text, 'books': house_books})


# Recommendations

@login_required
def recommendations(request):
    if request.user.is_staff:
        return JsonResponse({'error': 'Superusers are not allowed to access this view.'}, status=403)

    # Function that loads all user ratings for movies into the Prefs dictionary.
    # Also loads the inverse dictionary.
    # Serializes the results in dataRS.dat
    Prefs = {}   # {userid: {itemid: rating}}
    shelf = shelve.open("dataRS.dat")
    ratings = Rating.objects.all()
    for ra in ratings:
        userid = int(ra.userId.id)
        itemid = int(ra.characterId.id)
        rating = int(ra.rating)
        Prefs.setdefault(userid, {})
        Prefs[userid][itemid] = rating
    shelf['Prefs'] = Prefs
    shelf['ItemsPrefs'] = transformPrefs(Prefs)
    shelf['SimItems'] = calculateSimilarItems(Prefs, n=10)
    shelf.close()

    # Recommend characters to user based on their ratings
    items = None
    user = request.user

    if user.is_authenticated and user.id in Prefs:
        idUsuario = user.id
        shelf = shelve.open("dataRS.dat")
        Prefs = shelf['Prefs']
        shelf.close()
        recommendations = getRecommendations(Prefs, int(idUsuario))
        recommended = recommendations[: 3]
        characters = []
        ratings = []
        for re in recommended:
            characters.append(Character.objects.get(pk=re[1]))
            ratings.append(re[0])
        items = zip(characters, ratings)

    # Show similar character to one given
    character = None
    similar_items = None
    selected_character = request.GET.get('characters')

    shelf = shelve.open("dataRS.dat")
    ItemsPrefs = shelf['ItemsPrefs']
    shelf.close()
    characters = Character.objects.filter(id__in=ItemsPrefs.keys())
    if request.GET.get('characters'):
        character = get_object_or_404(Character, name=selected_character)
        characterId = character.id

        similar = topMatches(ItemsPrefs, int(characterId), n=3)
        characters = []
        similarity = []
        for re in similar:
            characters.append(Character.objects.get(pk=re[1]))
            similarity.append(re[0])
        similar_items = zip(characters, similarity)

    # Show users favourites and likes
    favourites = []
    liked_characters = []
    if user.is_authenticated and user.id in Prefs:
        favourites = Character.objects.filter(
            id__in=Rating.objects.filter(userId=user, rating=2).values_list('characterId', flat=True)
        )
        liked_characters = Character.objects.filter(
            id__in=Rating.objects.filter(userId=user, rating=1).values_list('characterId', flat=True)
        )

    return render(request, 'recommendations.html', {
        'items': items, 'user': user,
        'character': character, 'characters': characters, 'similar_items': similar_items,
        'favourites': favourites, 'liked_characters': liked_characters
    })
