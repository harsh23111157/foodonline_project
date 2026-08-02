from django import forms

from accounts.validators import allow_only_images_validator
from django.core.validators import FileExtensionValidator
from .models import Category, FoodItem  



class CategoryForm(forms.ModelForm):
  class Meta:
    model=Category
    fields=['Category_name','description']

class FoodItemForm(forms.ModelForm):
  image=forms.FileField(widget=forms.FileInput(attrs={'class':'btn btn-info w-100'}), validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp', 'jfif'])])
  class Meta:
    model=FoodItem
    fields=['category','Food_title','description','price','image','is_available']    