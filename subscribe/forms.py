from django import forms

from .models import Contact


class ContactForm(forms.ModelForm):
    """Форма подписки"""
    class Meta:
        model = Contact
        fields = ("email", )
        widgets = {
            "email": forms.TextInput(attrs={"name": "newsletter-mail", "id":"newsletter-mail", "placeholder": "email@example.com"})
        }

        labels ={
            "email": ""
        }