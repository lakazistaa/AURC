from django.urls import path
from . import views

urlpatterns = [
    path('', views.search_view, name='search_view'),
    path('more_details/', views.more_details, name='details'),
    path('about',views.about,name='about'),
    path('advanced',views.advanced_search_view,name='advanced_search_view'),
    path('stores',views.stores,name='stores'),
    path('ressources',views.ressources,name='ressources'),
    path('results',views.pagination_view,name='pagination_view'),
]
