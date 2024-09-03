from django.contrib import admin

# import models from models.py
from .models import Restaurant, Tag, Dish

# Register your models here.
# this will add the model to the admin panel

# inline class --> we use inline class to add a model to another model (1:m , m:m)

class DishInline(admin.TabularInline):
    model = Dish
    extra = 3

class RestaurantTagInline(admin.TabularInline):
    model = Tag.restaurants.through
    extra = 3

class RestaurantAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['name']}),
        (None,               {'fields': ['address']}),
        (None,               {'fields': ['latitude']}),
        (None,               {'fields': ['longitude']})
    ]

    inlines = [DishInline, RestaurantTagInline]
    list_display = ('name', 'address', 'latitude', 'longitude')

class TagAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['name']}),
    ]
    
    inlines = [RestaurantTagInline]


class DishAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['name']}),
        (None,               {'fields': ['description']}),
        (None,               {'fields': ['price']}),
        (None,               {'fields': ['restaurant']}),
    ]
    list_display = ('name', 'description', 'price', 'restaurant')

    
admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Dish, DishAdmin)
