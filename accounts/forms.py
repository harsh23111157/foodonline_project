from django import forms
from .models import User, UserProfile
from .validators import allow_only_images_validator
from django.core.validators import FileExtensionValidator

class UserForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput())
    confirm_password=forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model = User
        fields = ("first_name","last_name","username","email","password",)

    def clean(self):
        cleaned_data=super(UserForm,self).clean()
        password=cleaned_data.get('password')
        confirm_password=cleaned_data.get('confirm_password')


        if password != confirm_password:
            raise forms.ValidationError(
                "password doesnt match"
            )


class UserProfileForm(forms.ModelForm):
    address=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Start typing...','required':'required'}))
    profile_picture=forms.FileField(widget=forms.FileInput(attrs={'class':'btn btn-info w-100'}), validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp', 'jfif'])])
    cover_photo=forms.FileField(widget=forms.FileInput(attrs={'class':'btn btn-info w-100'}), validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp', 'jfif'])])

    class Meta:
        model = UserProfile
        fields = ("profile_picture","cover_photo","address","country","state","city","pin_code","latitude","longitude",)
        widgets = {
            "address": forms.TextInput(attrs={
                "id": "address",
                "class": "form-control",
                "autocomplete": "off",
                "placeholder": "Search your restaurant address"
            })
        }


    def __init__(self,*args,**kwargs):
        super(UserProfileForm,self).__init__(*args,**kwargs)
        for field in self.fields:
            if field == 'latitude' or field == 'longitude':
                self.fields[field].widget.attrs['readonly']='readonly'    

