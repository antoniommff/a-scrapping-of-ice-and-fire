# encoding:utf-8
import random
import shutil
import requests
from .progress import update_progress
from .models import House, Book
from bs4 import BeautifulSoup
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, KEYWORD
import os
import ssl


path = "db"
dirindex = "index"


def populate():
    from django.core.management import call_command
    call_command('migrate')
    populateHouses()
    populateBooks()
    # u = populateUsers()
    # m = populateMovies()
    # populateRatings(u, m)


if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
        getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context


def extract_house_data():
    pages = [
        ("https://hieloyfuego.fandom.com/wiki/"
         "Categoría:Casas_Nobles_de_Poniente"),
        ("https://hieloyfuego.fandom.com/wiki/"
         "Categoría:Casas_Nobles_de_Poniente?from=Casa+Hetherspoon"),
        ("https://hieloyfuego.fandom.com/wiki/"
         "Categoría:Casas_Nobles_de_Poniente?from=Casa+Torrent")
    ]

    i = 0
    total = 462
    update_progress(0, total, "Iniciando la carga de datos...")
    soups = []
    links = []

    for page in pages:
        response1 = requests.get(page)
        soup1 = BeautifulSoup(response1.text, 'html.parser')
        houses = soup1.find_all("a", class_="category-page__member-link")

        for h in houses:
            house = h['href']
            if "Categor%C3%ADa" in house:
                continue
            response2 = requests.get("https://hieloyfuego.fandom.com" + house)
            links.append("https://hieloyfuego.fandom.com" + house)
            soup2 = BeautifulSoup(response2.text, 'html.parser')
            soups.append(soup2)
            # print(f"Casa {house} extraída")
            update_progress(i + 1, total, f"Cargando casa {i + 1}/{total}")

    return soups, links


def populateHouses():

    # Delete tables
    if House.objects.exists():
        House.objects.all().delete()
    if Book.objects.exists():
        Book.objects.all().delete()

    # Load house pages
    houses = extract_house_data()[0]
    links = extract_house_data()[1]

    # Create schema for house text
    schem = Schema(
        name=TEXT(stored=True),
        words=TEXT(stored=True),
        lord=TEXT(stored=True),
        place=TEXT(stored=True),
        region=TEXT(stored=True),
        founder=TEXT(stored=True),
        text=TEXT(stored=True),
        books=KEYWORD(stored=True, commas=True)
    )

    if os.path.exists(dirindex):
        shutil.rmtree(dirindex)
    os.mkdir(dirindex)

    ix = create_in(dirindex, schema=schem)
    writer = ix.writer()
    i = 0

    # Scrap house data
    for h in houses:
        aside = h.find('div', class_='mw-parser-output')
        aside = aside.find('aside', role="region")
        if aside is None:
            continue

        name = aside.find('h2')
        name = name.get_text(strip=True)

        url = links[i]

        coat_tag = aside.find('figure', class_='pi-item pi-image')
        coat = coat_tag.a['href'] if coat_tag else None

        section = aside.find('section', class_='pi-group')
        words, place, lord, region, founder = None, None, None, None, None
        if section:
            data_items = section.find_all('div', class_="pi-item")
            for item in data_items:
                label = item.find('h3')
                value = item.find('div')
                if label and value:
                    if label.get_text(strip=True) == 'Lema':
                        words = value.get_text(strip=True)
                    elif label.get_text(strip=True) == 'Lugar':
                        place = value.get_text(strip=True)
                    elif label.get_text(strip=True) == 'Señor':
                        lord = value.get_text(strip=True)
                    elif label.get_text(strip=True) == 'Región':
                        region = value.get_text(strip=True)
                    elif label.get_text(strip=True) == 'Fundador':
                        founder = value.get_text(strip=True)

        paragraphs = h.find('div', class_='mw-parser-output').find_all("p")
        for p in paragraphs:
            possible_text = p.get_text(strip=True)
            if possible_text:
                text = possible_text
                continue

        reference_list = h.find('div', class_='mw-parser-output')\
            .find('div', class_='mw-references-wrap')
        if reference_list is None:
            continue
        reference_list = reference_list.find_all('span', class_='reference-text')
        books = []
        book_titles = set()
        for b in reference_list:
            book_tag = b.find('a')
            if book_tag and book_tag.get("title"):
                book_title = book_tag["title"]
                similar_book = None
                for existing_book in books:
                    if book_title.startswith(existing_book.title):
                        similar_book = existing_book
                        break
                    elif existing_book.title.startswith(book_title):
                        book_with_new_name = Book.objects.get(title=existing_book.title)
                        book_with_new_name.title = book_title
                        book_with_new_name.save()
                        break
                if similar_book:
                    book = similar_book
                else:
                    book, created = Book.objects.get_or_create(title=book_title)
                books.append(book)
                book_titles.add(book.title)

        # Create house
        house = House.objects.create(
            name=name, url=url, coat=coat, words=words, lord=lord, place=place, region=region, founder=founder
        )
        house.books.set(books)
        writer.add_document(
            name=str(name),
            words=str(words),
            lord=str(lord),
            place=str(place),
            region=str(region),
            founder=str(founder),
            text=str(text),
            books=str(", ".join(book_titles))
        )
        i += 1
        # print(f"Casa número {i} creada: {name}")

    # Create dictionary for RS {house_id:house_object}
    dict = {}
    for h in House.objects.all():
        dict[h.id] = h

    # Populate index
    writer.commit()
    # print("Fin de indexado", "Se han creado " + str(i) + " casas")
    update_progress(i, i, "¡Carga completa!")

    return (dict)


def populateBooks():
    ice_and_fire_titles = {
        "Juego de Tronos": "/covers/1_a_game_of_thrones.webp",
        "Choque de Reyes": "/covers/2_a_clash_of_kings.webp",
        "Tormenta de Espadas": "/covers/3_a_storm_of_swords.webp",
        "Festín de Cuervos": "/covers/4_a_feast_for_crows.webp",
        "Danza de Dragones": "/covers/5_a_dance_with_dragons.webp",
    }

    for book in Book.objects.all():

        # Correct some errors of the original page
        if book.title in ["Danza de Dragones-Apéndice", "A world of ice and fire"]:
            replacement_title = "Danza de Dragones" if book.title == "Danza de Dragones-Apéndice" else \
                "A World of Ice and Fire"
            replacement_book = Book.objects.get(title=replacement_title)
            for house in House.objects.filter(books=book):
                house.books.remove(book)
                house.books.add(replacement_book)
                house.save()
            book.delete()

        if book.title not in ["Juego de Tronos", "Choque de Reyes", "Tormenta de Espadas", "Festín de Cuervos",
                              "Danza de Dragones", "Vientos de Invierno", "Fuego y Sangre", "El Mundo de Hielo y Fuego",
                              "El Caballero de los Siete Reinos", "Los Hijos del Dragón", "La Espada Leal",
                              "El Príncipe Canalla", "El Caballero Errante", "El Caballero Misterioso",
                              "La Princesa y la Reina", "Los Príncipes de Poniente",
                              ]:
            book.delete()

        # Add cover to ice and fire saga books
        if book.title in ice_and_fire_titles:
            book.is_ice_and_fire = True
            book.cover = ice_and_fire_titles[book.title]
        else:
            book.cover = random.choice([
                "/covers/the_citadel_1.webp",
                "/covers/the_citadel_2.webp",
                "/covers/the_citadel_3.webp"
            ])
        book.save()
