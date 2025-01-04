from django.urls import path
from characters import views

urlpatterns = [
    path('data', views.data, name='data'),
    path('data_load', views.populateDatabase, name='data_load'),
    path('find', views.find, name='find'),

    path('houses', views.houses, name='houses'),
    path('get_house_text/', views.get_house_text_and_books, name='get_house_text'),
    path('get-progress/', views.get_load_progress, name='get_progress'),

    path('books', views.books, name='books'),

    path('characters', views.characters, name='characters'),

    path('recommendations', views.recommendations, name='recommendations'),
]
