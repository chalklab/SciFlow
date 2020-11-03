from django import forms
from datafiles.models import *
from datafiles.df_functions import json_validator


class UploadFileForm(forms.Form):
    # file = forms.FileField(validators=[json_validator])
    file = forms.FileField(validators=[json_validator], widget=forms.ClearableFileInput(attrs={'multiple': True}))
