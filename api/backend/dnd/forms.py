from django import forms

class ArtworkUploadForm(forms.Form):
    title = forms.CharField(max_length=255)
    file = forms.FileField()