from django.db import models

# Create your models here.

# we generally add all models to models.py file
# we can create a class for each table in the database

# restaurant table
class Restaurant(models.Model):
    name= models.CharField(max_length=30)
    address=models.CharField(max_length=100)
    latitude=models.FloatField(default=0)
    longitude=models.FloatField(default=0)
    
    # this function allow restaurant object to be displayed by its name in the admin panel
    def __str__(self):
        return self.name
    


# Tag table
# one tag can belong to multiple restaurants, one restaurant can have multiple tags --> may to many relationship
class Tag(models.Model):
    name= models.CharField(max_length=30, unique=True)
    restaurants= models.ManyToManyField(Restaurant)

    def __str__(self):
        return self.name


# Dish table

class Dish(models.Model):
    name=models.CharField(max_length=30)
    description=models.CharField(max_length=100)
    price=models.FloatField(default=0)
    restaurant=models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


# whenever we do any change in then we need to make migrations
# python manage.py makemigrations
# python manage.py migrate

