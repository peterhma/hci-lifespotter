from django.shortcuts import render
from coloring.models import *
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import ImageForm
import datetime
import pytz
import json
from rest_framework.decorators import api_view

from datetime import date, datetime

def get_author_by_name(authorname): 
  author = None
  
  # check if an Author with name 'authorname' already exists
  if Author.objects.filter(name = authorname).exists():
    # if so, fetch that object from the database
    author = Author.objects.get(name=authorname)
    
  else: 
    # otherwise, create a new Author with the name authorname
    author = Author(name = authorname, recently_used = "[]")
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
@api_view(['GET', 'POST'])
def sighting(request, id, authorname="DefaultAuthor"): 
  print("The authorname is:", authorname)
  author = get_author_by_name(authorname)
  
  print(request)
  
  if request.POST: 
  
    # POST request received
    
    # demonstrating printing out the POST request & data
    print("Received POST request with data:")

    if (id == "-1"): # id == -1 is only for sighting creation via the + button on the trip page.
      id = create_new_sighting(author)
      print("Created new sighting")
      print(id)
      return HttpResponse(id)
    
    elif Sighting.objects.filter(pk=id).exists(): # exist() sanity check, but this technically should never fail
      sighting = Sighting.objects.get(pk=id)
     # saving image
      data = request.data.keys()
      if request.data.get("image") or request.data.get("csrfmiddlewaretoken"):
        
        form = ImageForm(request.POST, request.FILES)
        print("POST IMAGE")
        if form.is_valid():
          form.save()
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
            "first_edit" : sighting.first_edit,
            "form" : form,
            "image" : form.instance.image.url,
          }  
  
          print(data["image"])
          
          # sighting.image = form.instance
          # sighting.save()
          
          return render(request, 'coloring/sighting_view.html', data)
        
      else:
        for key, value in request.data.items():
          data = json.loads(key)
       
        if "delete" in data:
          print("#DEBUG#", data)
          Sighting.objects.filter(pk=id).delete()
          return HttpResponse(True)
      # saving everything else
  
        sighting.name = data.get("name")
        sighting.species = data.get("species")
        sighting.date = data.get("date")
        sighting.time = data.get("time")
        sighting.latitude = data.get("latitude")
        sighting.longitude = data.get("longitude")
        sighting.notes = data.get("notes")
  
        sighting.first_edit = data.get("first_edit")
        sighting.image = data.get("image")



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

    #print(sighting.species)

    
    
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
      "first_edit" : sighting.first_edit,
      "image" : sighting.image,
    }
    return render(request, 'coloring/sighting_view.html', data)

def create_new_trip(author) -> int:
    trip = Trip(author=author,
                        name="",
                        desc= "");
    trip.save()
    print("Creating new trip:\n", trip.pk)
  

    return trip.pk

@csrf_exempt
def trip(request, id, authorname="DefaultAuthor"):
  print("The authorname is:", authorname)
  author = get_author_by_name(authorname)
  if id == "-1":
      if not request.POST: #must use post to create new
        return HttpResponse(False)
      id = create_new_trip(author)
      print("Created new trip")
      print(id)
      return HttpResponse(id)
  
  trip = Trip.objects.get(pk=id)
  
  if request.POST:
    # POST request received
    
    # demonstrating printing out the POST request & data
    print("Received POST request with data:")
    data = json.loads(request.body.decode('UTF-8'))
    print(data)
    
    if "delete" in data: #delete trip
      print("delete trip "+id)
      trip.remove();
      return HttpResponse(True)

    if 'sighting_id' in data: # modifiy sightings
      sighting = Sighting.objects.get(pk=data['sighting_id'])
      if 'remove_sighting' in data: #remove sighting
        sighting.trip = None
      else:
        sighting.trip = trip
      sighting.save()
          
    trip.name = data['name'];
    trip.desc = data['desc'];
    trip.save()

    return HttpResponse(True)

  else: 
    # GET request received

    #sightings = Sighting.objects.filter(author=author);
    sightings = Sighting.objects.filter(author=author, trip=trip);

    sightings = list(map(sighting_json, sightings));

    
    
    data = {
      "author": author,
      "trip": {
        "name": trip.name,
        "desc": trip.desc,
        "id": id,
        "sightings": sightings
      }
    }
    
    return render(request, 'coloring/trip_view.html', data)

@csrf_exempt
def species_info(request, species_id=0, authorname="DefaultAuthor", sid=0):
  # for now just render the page

  author = get_author_by_name(authorname)

  species_dict = []
  with open("coloring/static/species2.json") as d:
      species_dict = json.load(d)
  
  
  if request.POST:

    data = json.loads(request.body.decode('UTF-8'))

    ru_list = json.loads(author.recently_used)

    to_add = data["species_id"]
    
    if to_add in ru_list:
      ru_list.remove(to_add)

    ru_list.append(to_add)

    author.recently_used = str(ru_list);

    author.save()

    if Sighting.objects.filter(pk=sid).exists():
      sighting = Sighting.objects.get(pk=sid)
      sighting.species = species_dict[to_add]["name"]
      sighting.save()
    
    return HttpResponse(True)


  
  data = {
    "author": author,
    "info": species_dict[int(species_id)],
    "sid": sid
  }
  return render(request, 'coloring/species_view.html', data)

@csrf_exempt
def species_main(request, authorname="DefaultAuthor", sid=0):

  author = get_author_by_name(authorname)

  species_dict = []
  with open("coloring/static/species2.json") as d:
    species_dict = json.load(d)
    
  ru_list = json.loads(author.recently_used)
  
  ru_species = [species_dict[i] for i in ru_list[::-1]]
  
  data = {
    "author": author,
    "all_species": species_dict,
    "ru_species": ru_species,
    "sid": sid
  }
  
  return render(request, 'coloring/species_main.html', data)

@csrf_exempt
def species_key(request, authorname="DefaultAuthor", sid=0):

  author = get_author_by_name(authorname)  
  
  tree_dict = []
  with open('coloring/static/tree.json', "r") as d:
      tree_dict = json.load(d)
  
  data = {
    "author": author,
    "tree": tree_dict,
    "sid": sid
  }
  return render(request, 'coloring/species_key.html', data)

def sighting_json(obj, addtrip=False):
  author = {"name": obj.author.name};
  trip = '';
  if(addtrip and obj.trip):
    trip = {"author": author, "name": obj.trip.name, "desc": obj.trip.desc, "id": obj.trip.pk}
  
  return {
      "author": author,
      "name": obj.name if obj.name else "unnamed",
      "species": obj.species if obj.species else "",
      "date": str(obj.date),
      "time": str(obj.time),
      "latitude": obj.latitude,
      "longitude": obj.longitude,
      "notes": str(obj.notes),
      "image": str(obj.image),
    
      "id": obj.pk,
      "first_edit" : obj.first_edit,

      "trip": trip
    }

@csrf_exempt
def main(request, authorname="DefaultAuthor"):
  print("The authorname is:", authorname)
  author = get_author_by_name(authorname)
  
  if request.POST:
    data = json.loads(request.body.decode('UTF-8'))
    
    print("main post: ");
    west = data['west'];
    east = data['east'];
    south = data['south'];
    north = data['north'];
    
    sightings = None
    if east < west: #across the anti-meridian
      sightings = Sighting.objects.filter(author=author, longitude__gte=-180, longitude__lte=east, latitude__gte=south, latitude__lte=north);
      sightings = sightings.union(Sighting.objects.filter(author=author, longitude__gte=west, longitude__lte=180, latitude__gte=south, latitude__lte=north));
    else: #normal request
      sightings = Sighting.objects.filter(author=author, longitude__gte=west, longitude__lte=east, latitude__gte=south, latitude__lte=north);

    data = []
    
    for s in sightings:
      data.append(sighting_json(s, True));
    
    return HttpResponse(json.dumps(data));
  else:
    data = {
      "author": author
    }
    return render(request, 'coloring/main.html', data)