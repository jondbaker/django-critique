from django import forms

from .models import Critique


class CritiqueForm(forms.ModelForm):
    class Meta:
        fields = ("email", "message",)
        model = Critique
