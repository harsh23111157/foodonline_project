from django import forms
from .models import Vendor
from accounts.validators import allow_only_images_validator
from django.core.validators import FileExtensionValidator

class VendorForm(forms.ModelForm):
  vendor_license=forms.FileField(widget=forms.FileInput(attrs={'class':'btn btn-info w-100'}), validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp', 'jfif'])])
  class Meta:
    model=Vendor
    fields=['vendor_name','vendor_license']

    