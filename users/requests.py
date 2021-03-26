"""user request functions"""
from .models import Request


def makerequest(user, usertype, action, content, objectid):
    """make user creation request"""
    Request.objects.create(user=user, type=usertype, action=action,
                           content=content, object=objectid)


def rejectrequest(request):
    """reject user request"""
    if request.type == "Registration":
        user = request.user
        user.delete()
    request.delete()


def approverequest(request):
    """approve user request"""
    if request.type == "Registration":
        # TODO is this needed?
        user = request.user
    request.delete()
