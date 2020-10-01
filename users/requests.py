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
    request.delete()
