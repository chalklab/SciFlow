""" view definitions for the workflow app """
from django.shortcuts import render
from .wf_functions import *


def errors(response):
    """ for testing and displaying errorcodes"""

    if response.method == "POST":
        if 'errortest' in response.POST:
            errorcode = response.POST.get('errortest')
            adderror(2, errorcode)

    errs = readerrors(1)

    context = {"errors": errs}
    return render(response, "workflow/errors.html", context)
