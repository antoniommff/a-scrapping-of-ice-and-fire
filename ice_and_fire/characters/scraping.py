import os
import ssl
from .models import Book


if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
        getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context


def clean_text(element):
    return " ".join(element.stripped_strings)


ice_and_fire_books = ["Juego De Tronos", "Choque De Reyes", "Tormenta De Espadas", "Festín De Cuervos",
                      "Danza De Dragones", "Vientos De Invierno", "Fuego Y Sangre", "El Mundo De Hielo Y Fuego",
                      "El Caballero De Los Siete Reinos", "Los Hijos Del Dragón", "La Espada Leal",
                      "El Príncipe Canalla", "El Caballero Errante", "El Caballero Misterioso",
                      "La Princesa Y La Reina", "Los Príncipes De Poniente"
                      ]


def house_scrapping(h, link):
    aside = h.find('div', class_='mw-parser-output')
    aside = aside.find('aside', role="region")
    if aside is None:
        return None

    name = aside.find('h2')
    name = name.get_text(strip=True)

    url = link

    coat_tag = aside.find('figure', class_='pi-item pi-image')
    no_coat = "https://static-00.iconduck.com/assets.00/image-not-found-01-icon-512x512-a8erytww.png"
    coat = coat_tag.a['href'] if coat_tag else no_coat

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
        possible_text = clean_text(p)
        if possible_text:
            text = possible_text
            continue

    reference_list = h.find('div', class_='mw-parser-output')\
        .find('div', class_='mw-references-wrap')
    if reference_list is None:
        return None
    reference_list = reference_list.find_all('span', class_='reference-text')
    books = set()
    for b in reference_list:
        book_tag = b.find('a')
        if book_tag and book_tag.get("title"):
            book_title = book_tag["title"].title()
            if book_title in ice_and_fire_books:
                book, created = Book.objects.get_or_create(title=book_title)
                books.add(book)

    return name, url, coat, words, lord, place, region, founder, text, books


def character_scrapping(c, link):
    character_page = c[0]
    name = character_page.find("h1", class_="firstHeading")\
        .get_text(strip=True)
    url = link
    books = set()
    book_titles = set()
    paragraphs = character_page.find('div', class_='mw-parser-output')
    h3 = paragraphs.find_all('h3')
    for h in h3:
        book_title = h.text.title().replace('.', '')
        if (book_title != 'Antes De La Saga' and
           book_title != 'Primeros Años' and
           book_title != 'Trasfondo' and
           book_title != 'En La Obra' and
           not (book_title.endswith("Temporada"))):
            try:
                book = Book.objects.get(title=book_title)
                books.add(book)
                book_titles.add(book.title)
            except Book.DoesNotExist:
                print(f"Libro {book_title} no encontrado en la base de datos.")
    texts = paragraphs.find_all("p")
    for p in texts:
        possible_text = clean_text(p)
        if possible_text:
            text = possible_text
            break
    photo_page = c[1]
    photo = "https://static-00.iconduck.com/assets.00/image-not-found-01-icon-512x512-a8erytww.png"
    paragraphs = photo_page.find('div', class_='mw-parser-output')
    infobox = paragraphs.find('table', class_='infobox ib-character')
    if infobox:
        infobox_image = infobox.find("td", class_="infobox-image")
        if infobox_image:
            img_tag = infobox_image.find("img")
            if img_tag and 'src' in img_tag.attrs:
                photo = "https:" + img_tag['src']

    return name, url, text, photo, books, book_titles
