from django import forms
from .models import DriverProfile

class DriverProfileForm(forms.ModelForm):
    class Meta:
        model = DriverProfile
        fields = ['license_number', 'phone_number', 'vehicle_details', 'address']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }
