from django.shortcuts import render
from coloring.models import *
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import datetime
import pytz
import json

from datetime import date, datetime

def get_author_by_name(authorname): 
  author = None
  
  # check if an Author with name 'authorname' already exists
  if Author.objects.filter(name = authorname).exists():
    # if so, fetch that object from the database
    author = Author.objects.get(name=authorname)
    
  else: 
    # otherwise, create a new Author with the name authorname
    author = Author(name = authorname)
    # save the created object
    author.save()

  return author

def create_new_sighting(author) -> int:
    sighting = Sighting(author=author,
                        name="",
                        species= "",
                        date=date.today(),
                        time=datetime.now(pytz.timezone('US/Central')).strftime("%H:%M"), # cannot use utc because replit server places wrong timezone :(
                        latitude=30,
                        longitude= 97,
                        notes="")
    sighting.save()
    print("Creating new sighting:\n", sighting.date)
  

    return sighting.pk

@csrf_exempt
def index(request, authorname="DefaultAuthor"):

  print("The authorname is:", authorname)
  author = get_author_by_name(authorname)
  
  if request.POST: 
    # POST request received
    
    # demonstrating printing out the POST request & data
    print("Received POST request with data:")
    data = json.loads(request.body.decode('UTF-8'))
    print(data)

    
    return HttpResponse(True)

  else: 
    # GET request received

    data = {
      "author": author
    }
    
    return render(request, 'coloring/index.html', data)

@csrf_exempt
def sighting(request, id, authorname="DefaultAuthor"): 
  print("The authorname is:", authorname)
  author = get_author_by_name(authorname)
  
  print(request)
  
  if request.POST: 
    # POST request received
    
    # demonstrating printing out the POST request & data
    print("Received POST request with data:")
    data = json.loads(request.body.decode('UTF-8'))
    print(data)
  

    if (id == "-1"):
      id = create_new_sighting(author)
      print("Created new sighting")
      print(id)
      return HttpResponse(id)
    
    elif Sighting.objects.filter(pk=id).exists(): # exist() sanity check, but this technically should never fail
      sighting = Sighting.objects.get(pk=id)

      sighting.name = data["name"]
      sighting.species = data["species"]
      sighting.date = data["date"]
      sighting.time = data["time"]
      sighting.latitude = data["latitude"]
      sighting.longitude = data["longitude"]
      sighting.notes = data["notes"]

      sighting.first_edit = data["first_edit"]

      print("Updating existing sighting to id", id)
      sighting.save()
      
    else:
      print("ERROR: INVALID ID...")

    return HttpResponse(True)

  else:  # GET Request
    print("GET sighting id:", id)

    sighting = {}
    try:
      sighting = Sighting.objects.get(pk=id)
      print("Sighting exists, returning id", id)
    except ValueError:
      print("ERROR: No sighting with that ID exists. Must create the sighting first!")
        
    data = {
      "author": author,
      "name": sighting.name,
      "species": sighting.species,
      "date": sighting.date,
      "time": sighting.time,
      "latitude": sighting.latitude,
      "longitude": sighting.longitude,
      "notes": sighting.notes,

      "id": id,
      "first_edit" : sighting.first_edit
    }  
    return render(request, 'coloring/sighting_view.html', data)

@csrf_exempt
def trip(request, id, authorname="DefaultAuthor"):
  print("The authorname is:", authorname)
  author = get_author_by_name(authorname)
  
  if request.POST: 
    # POST request received
    
    # demonstrating printing out the POST request & data
    print("Received POST request with data:")
    data = json.loads(request.body.decode('UTF-8'))
    print(data)

    return HttpResponse(True)

  else: 
    # GET request received

    data = {
      "author": author
    }
    
    return render(request, 'coloring/trip_view.html', data)

@csrf_exempt
def species_info(request, species_id=0):
  # for now just render the page
  data = {}
  return render(request, 'coloring/species_view.html', data)

@csrf_exempt
def species_main(request, authorname="DefaultAuthor"):
  data = {}
  return render(request, 'coloring/species_main.html', data)

@csrf_exempt
def species_key(request):
  data = {}
  return render(request, 'coloring/species_key.html', data)

@csrf_exempt
def main(request, authorname="DefaultAuthor"):
  print("bruh mom")
  # for now just render the page
  data = {}
  return render(request, 'coloring/main.html', data)