from django import forms
from .models import Product, contact, Profile


class Productform(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'Owner_name', 'category', 'brand', 'image', 'image2', 'image3', 'image4', 'image5',
                  'Description', 'uploadfor', 'price', 'quantity', 'Condition', 'Feature1', 'Feature2', 'Feature3']


class Contactform(forms.ModelForm):
    class Meta:
        model = contact
        fields = '__all__'


class Profileform(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'address', 'pincode', 'country', 'state']
