from django import forms
from .models import ShippingAddress

class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['first_name', 'last_name', 'address', 'city', 'country', 'zip_code']