from django.shortcuts import render
from .populateDB import populate
from .progress import get_progress
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Book, Character, House
from whoosh.index import open_dir
from whoosh.qparser import MultifieldParser
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required

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
    houses = populate()  # Dictionary for RS {house_id:house_object}
    return render(request, 'load.html', {'message': 'Datos cargados con éxito', 'dict': houses})


@staff_member_required
@login_required
def get_load_progress(request):
    progress = get_progress()
    print(progress)
    return JsonResponse(progress)


@login_required
def data(request):
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
    query = request.GET.get('q')
    selected_book = request.GET.get('books')
    selected_house = request.GET.get('house')
    character_list = Character.objects.all()
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

    paginator = Paginator(character_list, CHARACTERS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'characters.html', {
        'page_obj': page_obj,
        'query': query,
        'books': Book.objects.all().order_by('title'),
        'houses': House.objects.all().order_by('name')
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

# @login_required
# def mark_book_as_read(request, book_id):
#     book = Book.objects.get(id=book_id)
#     user_book, created = UserBook.objects.get_or_create(user=request.user, book=book)
#     user_book.completed = True
#     user_book.save()
#     return redirect('recommendations')


def recommendations(request):
    # user_books = UserBook.objects.filter(user=request.user, completed=True)
    # read_books = [ub.book for ub in user_books]

    # recommended_books = Book.objects.exclude(id__in=[book.id for book in read_books])
    # houses = House.objects.filter(books__in=read_books).distinct()

    # return render(request, 'recommendations.html', {
    #     'houses': houses,
    #     'read_books': read_books,
    #     'recommended_books': recommended_books,
    # })
    return render(request, 'recommendations.html')
