from django import forms

class ImageUploadForm(forms.Form):
    """ Image upload form. """
    image_field = forms.ImageField()
