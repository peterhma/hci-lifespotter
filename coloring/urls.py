from django.urls import path
from . import views


urlpatterns = [
  path('main/<slug:authorname>/', views.main),
  path('sighting/<slug:authorname>/<slug:id>/', views.sighting),
  path('trip/<slug:authorname>/<slug:id>/', views.trip),
  path('species_info/<slug:authorname>/<slug:species_id>/<slug:sid>/', views.species_info),
  path('species/<slug:authorname>/<slug:sid>/', views.species_main),
  path('species_key/<slug:authorname>/<slug:sid>/', views.species_key),
  path('', views.index),
] 