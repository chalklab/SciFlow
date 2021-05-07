"""datafiles forms"""
from django import forms
from datafiles.df_functions import json_validator


class UploadFileForm(forms.Form):
    """ jsonld scidata file upload validator"""
    file = forms.FileField(validators=[json_validator], widget=forms.ClearableFileInput(attrs={'multiple': True}))
