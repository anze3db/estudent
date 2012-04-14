# Create your views here.
from django.contrib.auth import authenticate
from django.http import HttpResponse
from failedloginblocker.models import FailedAttempt
from student.models import Student
from warnings import catch_warnings
import json

def login(request):
    user = request.GET['id']
    response = { 'name': "", 'surname':"", 'login': False, 'numTries':0, 'errors':"" }
    try:
        fa = FailedAttempt.objects.get(username=user)

        if fa.recent_failure():
            if fa.too_many_failures():
                fa.failures += 1
                fa.save()
                response['numTries'] = fa.failures
                response['errors'] = "Too many login attempts."
                return HttpResponse(json.dumps(response), mimetype="application/json")
        
    except:
        fa = None
        
    auth = Student.authStudent(user, request.GET['password'])#None#authenticate(username=user, password=)
    
    if auth:
        response["name"] = auth.name
        response["surname"] = auth.surname
        response["login"] = True
    else:
        try:
            fa = FailedAttempt.objects.get(username=user)
        except:
            pass
        fa = fa or FailedAttempt( username=user, failures=0 )
        fa.failures += 1
        fa.save()
        response['numTries'] = fa.failures
        response['errors'] = "Wrong username or password."
                
    return HttpResponse(json.dumps(response), mimetype="application/json")


def _checkLoginTries(user, password):

    fa = FailedAttempt.objects.get( username=user )
    if fa.recent_failure( ):
        if fa.too_many_failures( ):
            # block the authentication attempt because
            # of too many recent failures
            fa.failures += 1
            fa.save( )
            return
            # raise LoginBlockedError( )
    else:
        # the block interval is over, reset the count
        fa.failures = 0
        fa.save( )
    # authentication failed 
    fa = fa or FailedAttempt( username=user, failures=0 )
    fa.failures += 1
    fa.save( )
    # return with unsuccessful auth
    return None