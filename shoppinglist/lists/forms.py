from django import forms

from .models import List

class ListCreateForm(forms.ModelForm):
   
    class Meta:
        model = List
        fields = ['name']
        widgets = {           
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'List Name', 'required': True}),
        }
   