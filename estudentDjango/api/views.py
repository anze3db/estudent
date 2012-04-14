# Create your views here.
from django.http import HttpResponse
from django.contrib.auth import authenticate
import json
from failedloginblocker.models import FailedAttempt
from warnings import catch_warnings

def login(request):
    user = request.GET['id']
    try:
        fa = FailedAttempt.objects.get(username=user)

        if fa.recent_failure():
            if fa.too_many_failures():
                fa.failures += 1
                fa.save()
                return HttpResponse("TOO MANYsss", mimetype="application/json")
        
    except:
        fa = None
        
    auth = None#authenticate(username=user, password=request.GET['password'])
    
    if auth:
        response = json.dumps(auth.id)
    else:
        try:
            fa = FailedAttempt.objects.get(username=user)
        except:
            pass
        fa = fa or FailedAttempt( username=user, failures=0 )
        fa.failures += 1
        fa.save()
        response = json.dumps(0)
    response = '(' + response + ');'
    
    return HttpResponse(response, mimetype="application/json")


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