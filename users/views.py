from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from .forms import RegisterForm
from django.contrib.auth import login
from .models import Request
from .requests import *


def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            content = {"Username":user.username, "Email":user.email, "First Name":user.first_name, "Last Name":user.last_name}
            makerequest(user, "Registration", "Registration", content, user.id)



            return redirect("/login")
    else:
        form = RegisterForm()

    return render(response, 'users/register.html', {"register":form})

class LoginView(View):
    def get(self, request):
        return render(request, 'registration/login.html', { 'form':  AuthenticationForm() })

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            try:
                form.clean()
            except ValidationError:
                return render(
                    request,
                    'registration/login.html',
                    { 'form': form, 'invalid_creds': True }
                )

            login(request, form.get_user())

            return redirect("/")

        return render(request, 'registration/login.html', { 'form': form })

class ConfirmRegistrationView(View):
    def get(self, request, user_id, token):
        user_id = force_text(urlsafe_base64_decode(user_id))

        user = User.objects.get(pk=user_id)

        context = {
          'form': AuthenticationForm(),
          'message': 'Registration confirmation error. Please click the reset password to generate a new confirmation email.'
        }
        if user and user_tokenizer.check_token(user, token):
            user.is_active = True
            user.save()
            context['message'] = 'Registration complete. Please login'

        return render(request, 'home.html', context)



def requests(response):
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

    return render(response, 'users/requests.html', {"request":request, "allrequests":allrequests})
