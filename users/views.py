"""user app views functions"""
from django.shortcuts import render, redirect
# åfrom social_core.exceptions import AuthFailed

from .requests import Request, approverequest, rejectrequest
from django.contrib.auth.decorators import login_required
import json
from django.contrib.auth import logout as log_out
from django.conf import settings
from django.http import HttpResponseRedirect
from urllib.parse import urlencode


def index(request):
    """index page"""
    user = request.user
    if user.is_authenticated:
        return redirect(dashboard)
    else:
        return render(request, 'users/index.html')


def error(request):
    """error page"""
    return render(request, 'users/error.html')


@login_required
def dashboard(request):
    """dashboard page"""
    user = request.user
    # TODO social_auth unresolved (linked to used import above?)
    auth0user = user.social_auth.get(provider='auth0')
    userdata = {
        'user_id': auth0user.uid,
        'name': user.first_name,
        'picture': auth0user.extra_data['picture'],
        'email': auth0user.extra_data['email'],
    }
    return render(request, 'users/dashboard.html', {
        'auth0User': auth0user, 'userdata': json.dumps(userdata, indent=4)})


def requests(response):
    """requests page"""
    request = Request.objects.first()
    allrequests = Request.objects.all()

    if response.method == "POST":
        for k in response.POST:
            if 'approve' in k:
                rid = k.split("_")[1]
                request = request.object.get(id=rid)
                approverequest(request)
            if 'reject' in k:
                rid = k.split("_")[1]
                request = request.object.get(id=rid)
                rejectrequest(request)

    return render(response, 'users/requests.html',
                  {"request": request, "allrequests": allrequests})


def logout(request):
    """logout processing"""
    log_out(request)
    return_to = urlencode({'returnTo': request.build_absolute_uri('/')})
    logout_url = 'https://%s/v2/logout?client_id=%s&%s' % \
                 (settings.SOCIAL_AUTH_AUTH0_DOMAIN,
                  settings.SOCIAL_AUTH_AUTH0_KEY, return_to)
    return HttpResponseRedirect(logout_url)
