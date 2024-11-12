from django import forms
from .models import Character

class ArtworkUploadForm(forms.Form):
    title = forms.CharField(max_length=255)
    file = forms.FileField()


class CharacterForm(forms.ModelForm):
    class Meta:
        model = Character
        fields = ["name", "initiative", "dexterity"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Character Name"}),
            "initiative": forms.NumberInput(attrs={"placeholder": "Initiative"}),
            "dexterity": forms.NumberInput(attrs={"placeholder": "Dexterity"}),
        }
