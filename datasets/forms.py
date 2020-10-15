from django import forms
from datasets.models import *


class UploadFileForm(forms.Form):
    file = forms.FileField(validators=[json_validator])