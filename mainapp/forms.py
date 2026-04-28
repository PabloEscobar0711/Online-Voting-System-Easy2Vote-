from django import forms
from .models import Query

class QueryForm(forms.ModelForm):
    class Meta:
        model = Query
        fields = ['name', 'email', 'branch', 'query']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your email'}),
            'branch': forms.Select(attrs={'class': 'form-control'}),
            'query': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your message'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your email'}),
        }