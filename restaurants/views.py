from django.http import HttpResponse
from django.core import serializers
from django.http import Http404, HttpResponseNotAllowed
from .models import Restaurant, Dish, Tag
import json

from django.views.decorators.csrf import csrf_exempt

# Create your views here.

# add new restaurant service
@csrf_exempt # Disable CSRF protection for this view
def create_a_new_restaurant(request):
    if request.method == 'POST':  # Check if the request method is POST
        body = json.loads(request.body.decode('utf-8'))  # Parse the JSON body of the request
        new_name = body.get("name")  # Extract the 'name' field from the JSON body
        new_address = body.get("address")  # Extract the 'address' field from the JSON body
        new_latitude = body.get("latitude")  # Extract the 'latitude' field from the JSON body
        new_longitude = body.get("longitude")  # Extract the 'longitude' field from the JSON body
        try:
            tag = Tag.objects.get(pk=body.get("tag_id"))  # Try to get the Tag object with the given 'tag_id'
        except Tag.DoesNotExist:
            raise Http404("tag not exist")  # Raise a 404 error if the Tag does not exist
        new_restaurant = Restaurant(
            name=new_name,
            address=new_address,
            latitude=new_latitude,
            longitude=new_longitude
        )  # Create a new Restaurant object with the extracted data
        new_restaurant.save()  # Save the new Restaurant object to the database
        tag.restaurants.add(new_restaurant)  # Add the new Restaurant to the Tag's restaurants
        tag.save()  # Save the Tag object to update the relationship
        return HttpResponse(status=200)  # Return a 200 OK response
    else:
        return HttpResponseNotAllowed("Method Not Allowed")  # Return a 405 Method Not Allowed response if the method is not POST
    


# get all restaurant
def get_all_restaurant(request):
    if(request.method=='GET'):
        restaurant= Restaurant.objects.all()
        data= serializers.serialize("json", restaurant)
        return HttpResponse(data)


# get a restaurant by id
def get_restaurant_by_id(request, restaurant_id):
    if(request.method=='GET'):
        restaurant= Restaurant.objects.filter(pk=restaurant_id)
        if(restaurant is None):
            raise Http404("restaurant not exist")
        
        data= serializers.serialize("json", restaurant)
        return HttpResponse(data)

# update a restaurant by id
@csrf_exempt # Disable CSRF protection for this view
def update_restaurant_by_id(request, restaurant_id):
    if request.method == 'PUT':
        body = json.loads(request.body.decode('utf-8'))
        new_name = body.get("name")
        new_address = body.get("address")
        new_latitude = body.get("latitude")
        new_longitude = body.get("longitude")
        try:
            tag = Tag.objects.get(pk=body.get("tag_id"))
        except Tag.DoesNotExist:
            raise Http404("Tag does not exist")
        try:
            restaurant = Restaurant.objects.get(pk=restaurant_id)
        except Restaurant.DoesNotExist:
            raise Http404("Restaurant does not exist")
        restaurant.name = new_name
        restaurant.address = new_address
        restaurant.latitude = new_latitude
        restaurant.longitude = new_longitude
        restaurant.save()
        tag.restaurants.add(restaurant)
        tag.save()
        return HttpResponse(status=200)
    else:
        raise HttpResponseNotAllowed("Method is not supported")


# delete a restaurant by id
def delete_restaurant_by_id(request, restaurant_id):
    if request.method == 'DELETE':
        try:
            restaurant = Restaurant.objects.get(pk=restaurant_id)
        except Restaurant.DoesNotExist:
            raise Http404("Restaurant does not exist")
        
        restaurant.delete()
        return HttpResponse(status=200)
    else:
        raise HttpResponseNotAllowed("Method is not supported")