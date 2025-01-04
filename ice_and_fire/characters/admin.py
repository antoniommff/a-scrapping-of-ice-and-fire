from django.contrib import admin

from .models import House, Book, Character

admin.site.register(Book)
admin.site.register(House)
admin.site.register(Character)
