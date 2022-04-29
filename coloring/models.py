from django.db import models
from datetime import date, datetime
from django.conf import settings

# The Author model has been created for you
class Author(models.Model):
  name = models.CharField(max_length=50)
  
class Trip(models.Model):
  author = models.ForeignKey(Author, on_delete=models.CASCADE)
  name = models.CharField(max_length=50)
  desc = models.TextField()
  
class Sighting(models.Model):
  author = models.ForeignKey(Author, on_delete=models.CASCADE)
  
  name = models.CharField(max_length=50)
  species = models.TextField()
  longitude = models.FloatField()
  latitude = models.FloatField()
  date = models.DateField(default=date.today())
  time = models.TimeField(default=datetime.now().strftime("%H:%M:%S"))
  notes = models.TextField()
  
  # otm, trip that sighting belongs to. To get sightings of a specific trip, do
  # t.sightings.all(). Same with species.
  trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name="sighting", null=True, blank=True) 

  first_edit = models.IntegerField(default=1)
# Create the Drawing model

