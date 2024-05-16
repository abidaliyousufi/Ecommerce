from django.contrib import admin
from .models import Products,Comments
# Register your models here.
@admin.register(Products)
class ProductAdmin(admin.ModelAdmin):
  list_display = ['id','title','description','image','price']


@admin.register(Comments)
class ProductAdmin(admin.ModelAdmin):
  list_display = ['id','comment','user','product_id']