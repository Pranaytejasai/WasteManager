from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, Address

class UserProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['address', 'address_type', 'city', 'state', 'postal_code']