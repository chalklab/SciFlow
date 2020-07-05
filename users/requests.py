from django.core.mail import send_mail
from django.template.loader import get_template
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .models import Request

def makerequest(user, type, action, content, objectid):
    print(user)
    print(type)
    print(action)
    print(content)
    print(objectid)
    Request.objects.create(user=user, type=type, action=action, content=content, object=objectid)

def rejectrequest(request):
    if request.type == "Registration":
        user = request.user
        user.delete()
    request.delete()

def approverequest(request):
    if request.type == "Registration":
        user = request.user
        #token = user_tokenizer.make_token(user)
        #user_id = urlsafe_base64_encode(force_bytes(user.id))
        #url = 'http://localhost:8000' + reverse('confirm_email', kwargs={'user_id': user_id, 'token': token})
        #message = get_template('users/register_email.html').render({'confirm_url': url, 'user': user})
        #send_mail('Beekeeper Email Confirmation', message, 'sciflow@gmail.com', [user.email], fail_silently=False)
    request.delete()
