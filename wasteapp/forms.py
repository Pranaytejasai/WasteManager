from django import forms
from .models import WasteRequest
from profileapp.models import Address

class WasteRequestForm(forms.ModelForm):
    collection_location = forms.ModelChoiceField(
        queryset=Address.objects.none(),  # Dynamically populated
        required=False,  # Allow fallback to default address
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = WasteRequest
        fields = ['waste_type', 'quantity', 'collection_time', 'collection_location']
        widgets = {
            'collection_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Extract user from kwargs
        super().__init__(*args, **kwargs)
        
        # Dynamically set the queryset for `collection_location`
        if user:
            self.fields['collection_location'].queryset = Address.objects.filter(user=user)
        else:
            self.fields['collection_location'].queryset = Address.objects.none()
