from django.urls import path
from . import views

urlpatterns = [
    path('', views.random_quote, name='random_quote'),
    path('add/', views.add_quote, name='add_quote'),
    path('popular/', views.popular_quotes, name='popular_quotes'),
    path('search/', views.search_quotes, name='search_quotes'),
    path('vote/<int:quote_id>/<str:vote_type>/', views.vote, name='vote'),
]