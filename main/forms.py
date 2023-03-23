from django import forms

from . import models

class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = models.Profile
        fields = ['profile_image']