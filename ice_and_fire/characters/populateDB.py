# encoding:utf-8
import random
import shutil
import requests
from .scraping import character_scrapping, house_scrapping
from users.models import CustomUser
from .progress import update_progress
from .models import Character, House, Book, Rating
from bs4 import BeautifulSoup
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, KEYWORD
import os
import ssl
from datetime import datetime


sample_data_path = "sample_data"
path = "db"
dirindex1 = "index1"
dirindex2 = "index2"
ice_and_fire_books = ["Juego De Tronos", "Choque De Reyes", "Tormenta De Espadas", "Festín De Cuervos",
                      "Danza De Dragones", "Vientos De Invierno", "Fuego Y Sangre", "El Mundo De Hielo Y Fuego",
                      "El Caballero De Los Siete Reinos", "Los Hijos Del Dragón", "La Espada Leal",
                      "El Príncipe Canalla", "El Caballero Errante", "El Caballero Misterioso",
                      "La Princesa Y La Reina", "Los Príncipes De Poniente"
                      ]


def populate():
    from django.core.management import call_command
    call_command('migrate')

    # populateUsers(sample_data_path)

    populateHouses()
    populateBooks()
    populateCharacters()

    populateRatings(sample_data_path)


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
    total = 462 + 55 + 60

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


def populateUsers(file_path):
    # Delete tables
    CustomUser.objects.exclude(username='admin').delete()

    fileobj = open(file_path+"/users.txt", "r")
    for line in fileobj.readlines():
        rip = str(line.strip()).split('|')

        CustomUser.objects.create_user(
            name=rip[1],
            surname=rip[2],
            email=rip[3],
            username=rip[4],
            password=rip[5],
        )
        user = CustomUser.objects.get(username=rip[4])
        print(f"Usuario {user.username} creado con id: {user.id}")

    fileobj.close()
    print("---¡Se han creado todos los usuarios!---")


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

    if os.path.exists(dirindex1):
        shutil.rmtree(dirindex1)
    os.mkdir(dirindex1)

    ix1 = create_in(dirindex1, schema=schema1)
    writer1 = ix1.writer()
    i = 0

    # Scrap house data
    for h in houses:
        if house_scrapping(h, links[i]) is None:
            continue
        name, url, coat, words, lord, place, region, founder, text, books = house_scrapping(h, links[i])

        # Create house
        new_house = House.objects.create(
            name=name, url=url, coat=coat, words=words, lord=lord, place=place, region=region, founder=founder
        )
        new_house.books.set(books)
        writer1.add_document(
            name=str(name),
            words=str(words),
            lord=str(lord),
            place=str(place),
            region=str(region),
            founder=str(founder),
            text=str(text),
            books=str(", ".join([book.title for book in books]))
        )
        i += 1

    # Populate index
    writer1.commit()
    print("---¡Se han creado todas las casas!---")


def populateBooks():
    ice_and_fire_titles = {
        "Juego De Tronos": "/covers/1_a_game_of_thrones.webp",
        "Choque De Reyes": "/covers/2_a_clash_of_kings.webp",
        "Tormenta De Espadas": "/covers/3_a_storm_of_swords.webp",
        "Festín De Cuervos": "/covers/4_a_feast_for_crows.webp",
        "Danza De Dragones": "/covers/5_a_dance_with_dragons.webp",
    }

    ice_and_fire_dates = {
        "Juego De Tronos": "1996-08-06",
        "Choque De Reyes": "1998-11-16",
        "Tormenta De Espadas": "2000-08-08",
        "Festín De Cuervos": "2005-11-08",
        "Danza De Dragones": "2011-07-12",
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

        # Add cover and date to ice and fire saga books
        if book.title in ice_and_fire_titles:
            book.is_ice_and_fire = True
            book.cover = ice_and_fire_titles[book.title]
            book.date = datetime.strptime(ice_and_fire_dates[book.title], "%Y-%m-%d").date()
        else:
            book.cover = random.choice([
                "/covers/the_citadel_1.webp",
                "/covers/the_citadel_2.webp",
                "/covers/the_citadel_3.webp"
            ])
        book.save()

    print("---¡Se han creado todos los libros!---")


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
        house=TEXT(stored=True),
        books=KEYWORD(stored=True, commas=True)
    )

    if os.path.exists(dirindex2):
        shutil.rmtree(dirindex2)
    os.mkdir(dirindex2)

    ix2 = create_in(dirindex2, schema=schema2)
    writer2 = ix2.writer()
    i = 0

    # Scrap character data
    for c in characters:
        if character_scrapping(c, links[i]) is None:
            continue
        name, url, text, photo, books, book_titles = character_scrapping(c, links[i])

        # Create character
        character = Character.objects.create(
            name=name, url=url, photo=photo
        )
        character.books.set(books)

        last_name = name.split()[-1]
        house = House.objects.filter(name__icontains=(" " + last_name))
        if house and "Caminante" not in name:
            character.house = house[0]
            character.save()

        writer2.add_document(
            name=str(name),
            text=str(text),
            house=str(house[0].name) if house else "Sin casa reconocida",
            books=str(", ".join(book_titles))
        )
        i += 1

    # Populate index
    writer2.commit()
    print("---¡Se han creado todos los personajes!---")
    print("Fin de indexado", "Se han creado " + str(i) + " elementos")
    update_progress(462+i, 462+i, "¡Carga completa!")


def populateRatings(file_path):
    # Delete tables
    if Rating.objects.exists():
        Rating.objects.all().delete()

    u = CustomUser.objects.all()
    c = Character.objects.all()

    fileobj = open(file_path+"/ratings.txt", "r")
    for line in fileobj.readlines():
        rip = str(line.strip()).split('|')
        rating = Rating.objects.create(userId=u[int(rip[0])], characterId=c[int(rip[1])], rating=int(rip[2]))
        print(f"Puntuación ({rating.userId}, {rating.characterId}) creado")

    fileobj.close()
    print("---¡Se han creado todos los ratings!---")
