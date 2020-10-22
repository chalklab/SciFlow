""" view definitions for the workflow app """
from datafiles.forms import *
from django.shortcuts import redirect
from django.shortcuts import render
from .wf_functions import *


def errors(response):
    """ for testing and displaying errorcodes"""

    if response.method == "POST":
        if 'errortest' in response.POST:
            errorcode = response.POST.get('errortest')
            adderror(2,errorcode)

    errors = readerrors(1)

    context = {"errors":errors}
    return render(response, "workflow/errors.html", context)
