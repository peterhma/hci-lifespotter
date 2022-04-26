from django.urls import path
from . import views

urlpatterns = [
  path('main/<slug:authorname>/', views.main),
  path('sighting/<slug:authorname>/<slug:id>/', views.sighting),
  path('trip/<slug:authorname>/<slug:id>/', views.trip),
  path('species_info/<slug:species_id>/', views.species_info),
  path('species/<slug:authorname>/', views.species_main),
  path('species_key/', views.species_key),
  path('', views.index),
]
