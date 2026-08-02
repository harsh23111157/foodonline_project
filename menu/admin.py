from django.contrib import admin
from .models import Category,FoodItem
# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
  list_display=('Category_name','vendor','slug','created_at','updated_at')
  prepopulated_fields={'slug':('Category_name',)}
  search_fields=('Category_name','vendor__vendor_name')

@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
  list_display=('Food_title','category','slug','price','is_available','created_at','updated_at')
  prepopulated_fields={'slug':('Food_title',)}
  search_fields=('Food_title','category__Category_name','vendor__vendor_name','price')
  list_filter=('is_available',)