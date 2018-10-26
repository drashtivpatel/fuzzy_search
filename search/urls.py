from django.urls import path
from .views import search

url_patterns = [
    path('search', search, name='search'),
]