from django.urls import path
from django.shortcuts import redirect
from users import views

urlpatterns = [
    path('', lambda request: redirect('login/')),
    path('login/', views.login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('delete_account/', views.delete_account, name='delete_account'),
]
