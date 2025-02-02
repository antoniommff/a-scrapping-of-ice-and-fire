from django.urls import path
from characters import views

urlpatterns = [
    path('', views.home, name='home'),

    path('data', views.data, name='data'),
    path('data_load', views.populateDatabase, name='data_load'),
    path('get-progress/', views.get_load_progress, name='get_progress'),

    path('find', views.find, name='find'),

    path('houses', views.houses, name='houses'),
    path('get_house_text/', views.get_house_text_and_books, name='get_house_text'),

    path('books', views.books, name='books'),

    path('characters', views.characters, name='characters'),
    path('get_character_text/', views.get_character_text_books_and_house, name='get_character_text'),

    path('recommendations', views.recommendations, name='recommendations'),
    path('add_to_favorites/', views.add_to_favorites, name='add_to_favorites'),
    path('add_to_likes/', views.add_to_likes, name='add_to_likes'),
    path('remove_from_favorites/', views.remove_from_favorites, name='remove_from_favorites'),
    path('remove_from_likes/', views.remove_from_likes, name='remove_from_likes'),
]
