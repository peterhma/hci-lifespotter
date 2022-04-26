from django.shortcuts import render
from coloring.models import *
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

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