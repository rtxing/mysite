from django import forms
from carshops.models import Carshop

class CarShopForm(forms.ModelForm):
    class Meta:
        model = Carshop
        fields = ['opening_time', 'closing_time']
        widgets = {
            'opening_time': forms.TimeInput(attrs={'type': 'time'}),
            'closing_time': forms.TimeInput(attrs={'type': 'time'}),
        }
