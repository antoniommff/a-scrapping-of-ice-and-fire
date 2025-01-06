from django.contrib import admin

from .models import House, Book, Character, Rating

admin.site.register(Book)
admin.site.register(House)
admin.site.register(Character)
admin.site.register(Rating)
