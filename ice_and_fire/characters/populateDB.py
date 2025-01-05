# encoding:utf-8
import random
import shutil
import requests
from .progress import update_progress
from .models import Character, House, Book
from bs4 import BeautifulSoup
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, KEYWORD
import os
import ssl


path = "db"
dirindex = "index"
ice_and_fire_books = ["Juego De Tronos", "Choque De Reyes", "Tormenta De Espadas", "Festín De Cuervos",
                      "Danza De Dragones", "Vientos De Invierno", "Fuego Y Sangre", "El Mundo De Hielo Y Fuego",
                      "El Caballero De Los Siete Reinos", "Los Hijos Del Dragón", "La Espada Leal",
                      "El Príncipe Canalla", "El Caballero Errante", "El Caballero Misterioso",
                      "La Princesa Y La Reina", "Los Príncipes De Poniente"
                      ]


def populate():
    from django.core.management import call_command
    call_command('migrate')
    populateHouses()
    populateBooks()
    populateCharacters()
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
    total = 462 + 55
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
            print(f"{house.replace("/wiki/", "").replace("_", " ")} extraída")
            update_progress(i + 1, total, f"Cargando casa {i + 1}/{total}")

    return soups, links


def extract_character_data():
    page = ("https://es.wikipedia.org/wiki/"
            "Categoría:Personajes_de_Canción_de_hielo_y_fuego")
    soups = []
    links = []
    i = 462
    total = 462 + 55

    response1 = requests.get(page)
    soup1 = BeautifulSoup(response1.text, 'html.parser')
    characters = soup1.find("div", class_="mw-category mw-category-columns") \
                      .find_all('a', href=True)

    for c in characters:
        character = c['href']
        if character == '/wiki/Anexo:Personajes_de_Canci%C3%B3n_de_hielo_y_fuego':
            continue
        response2 = requests.get("https://es.wikipedia.org" + character)
        character_en = character.replace('Arena', 'Sand').replace('Nieve', 'Snow')
        response3 = requests.get("https://en.wikipedia.org" + character_en)
        links.append("https://es.wikipedia.org" + character)
        soup2 = BeautifulSoup(response2.text, 'html.parser')
        soup3 = BeautifulSoup(response3.text, 'html.parser')
        soups.append((soup2, soup3))
        print(f"Personaje {character.replace("/wiki/", "").replace("_", " ")} extraído")
        update_progress(i + 1, total, f"Cargando personaje {i + 1}/{total}")

    return soups, links


def populateHouses():

    # Delete tables
    if House.objects.exists():
        House.objects.all().delete()
    if Book.objects.exists():
        Book.objects.all().delete()

    # Load house pages
    data = extract_house_data()
    houses = data[0]
    links = data[1]

    # Create schema for house text
    schema1 = Schema(
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

    ix1 = create_in(dirindex, schema=schema1)
    writer1 = ix1.writer()
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
        books = set()
        book_titles = set()
        for b in reference_list:
            book_tag = b.find('a')
            if book_tag and book_tag.get("title"):
                book_title = book_tag["title"].title()
                if book_title in ice_and_fire_books:
                    book, created = Book.objects.get_or_create(title=book_title)
                    books.add(book)
                    book_titles.add(book.title)

        # Create house
        house = House.objects.create(
            name=name, url=url, coat=coat, words=words, lord=lord, place=place, region=region, founder=founder
        )
        house.books.set(books)
        writer1.add_document(
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
    writer1.commit()
    # print("Fin de indexado", "Se han creado " + str(i) + " casas")

    return (dict)


def populateBooks():
    ice_and_fire_titles = {
        "Juego De Tronos": "/covers/1_a_game_of_thrones.webp",
        "Choque De Reyes": "/covers/2_a_clash_of_kings.webp",
        "Tormenta De Espadas": "/covers/3_a_storm_of_swords.webp",
        "Festín De Cuervos": "/covers/4_a_feast_for_crows.webp",
        "Danza De Dragones": "/covers/5_a_dance_with_dragons.webp",
    }

    for book in Book.objects.all():

        # Correct some errors of the original page
        if book.title in ["Danza De Dragones-Apéndice", "A World Of Ice And Fire"]:
            replacement_title = "Danza De Dragones" if book.title == "Danza de Dragones-Apéndice" else \
                "El Mundo De Hielo Y Fuego"
            replacement_book = Book.objects.get(title=replacement_title)
            for house in House.objects.filter(books=book):
                house.books.remove(book)
                house.books.add(replacement_book)
                house.save()
                Book.objects.filter(title=book.title).delete()

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

    for book in Book.objects.all():
        print(f"Libro {book.title} creado")


def populateCharacters():

    # Delete tables
    if Character.objects.exists():
        Character.objects.all().delete()

    # Load house pages
    data = extract_character_data()
    characters = data[0]
    links = data[1]

    # Create schema for house text
    schema2 = Schema(
        name=TEXT(stored=True),
        text=TEXT(stored=True),
        books=KEYWORD(stored=True, commas=True)
    )

    if os.path.exists(dirindex):
        shutil.rmtree(dirindex)
    os.mkdir(dirindex)

    ix2 = create_in(dirindex, schema=schema2)
    writer2 = ix2.writer()
    i = 0

    # Scrap character data
    for c in characters:
        character_page = c[0]
        name = character_page.find("h1", class_="firstHeading")\
            .get_text(strip=True)

        url = links[i]

        books = set()
        book_titles = set()
        paragraphs = character_page.find('div', class_='mw-parser-output')
        h3 = paragraphs.find_all('h3')
        for h in h3:
            book_title = h.text.title()
            if (book_title != 'Antes De La Saga' and
               book_title != 'Primeros Años' and
               book_title != 'Trasfondo' and
               book_title != 'En La Obra' and
               not (book_title.endswith("Temporada"))):
                print(book_title)
                try:
                    book = Book.objects.get(title=book_title)
                    books.add(book)
                    book_titles.add(book.title)
                except Book.DoesNotExist:
                    print(f"Libro {book_title} no encontrado en la base de datos.")

        texts = paragraphs.find_all("p")
        for p in texts:
            possible_text = p.get_text(strip=True)
            if possible_text:
                text = possible_text
                break

        photo_page = c[1]
        photo = ""
        paragraphs = photo_page.find('div', class_='mw-parser-output')
        infobox = photo_page.find('table', class_='infobox')
        if infobox:
            photo = infobox.a['href']

        # Create character
        character = Character.objects.create(
            name=name, url=url, photo=photo
        )
        character.books.set(books)
        writer2.add_document(
            name=str(name),
            text=str(text),
            books=str(", ".join(book_titles))
        )
        i += 1
        # print(f"Personaje número {i} creado: {name}")

    # Create dictionary for RS {house_id:house_object}
    dict = {}
    for h in House.objects.all():
        dict[h.id] = h

    # Populate index
    writer2.commit()
    # print("Fin de indexado", "Se han creado " + str(i) + " casas")
    update_progress(i, i, "¡Carga completa!")

    return (dict)
