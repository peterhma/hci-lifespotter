from django.db import models
from datetime import date, datetime
from django.conf import settings

# The Author model has been created for you
class Author(models.Model):
  name = models.CharField(max_length=50)
  recently_used = models.TextField()
  
class Trip(models.Model):
  author = models.ForeignKey(Author, on_delete=models.CASCADE)
  name = models.CharField(max_length=50)
  desc = models.TextField()

  
class Sighting(models.Model):
  author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True)

  image =models.ImageField(default="/images/default.jpg", null=True)
  name = models.CharField(max_length=50, null=True)
  species = models.TextField(null=True)
  date = models.DateField(default=date.today())
  time = models.TimeField(default=datetime.now().strftime("%H:%M:%S"))
  longitude = models.FloatField(null=True)
  latitude = models.FloatField(null=True)
  notes = models.TextField(null=True)
  
  # otm, trip that sighting belongs to. To get sightings of a specific trip, do
  # t.sightings.all(). Same with species.
  trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name="sighting", null=True, blank=True) 

  first_edit = models.IntegerField(default=1)
# Create the Drawing model

