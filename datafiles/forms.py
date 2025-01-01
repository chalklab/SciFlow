"""datafiles forms"""
from django import forms
from datafiles.df_functions import json_validator

LOCALE_CHOICES = [
    ('remote', 'Remote'),
    ('local', 'Local'),
]


class UploadFileForm(forms.Form):
    """ jsonld scidata file upload validator"""
    file = forms.FileField(validators=[json_validator], widget=forms.ClearableFileInput())
    # locale = forms.CharField(widget=forms.RadioSelect(LOCALE_CHOICES, initial='remote'))
