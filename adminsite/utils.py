from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from adminsite.usermanagement.models import USER_TYPE
from vehiclemanagement import settings

def admin_access_required():
    def wrapper(function):
        @login_required(login_url=settings.ADMIN_LOGIN_URL)
        def wrap(request, *args, **kwargs):
            if request.user.type == USER_TYPE.ADMIN:
                return function(request, *args, **kwargs)
            return redirect(settings.ADMIN_LOGIN_URL)
        return wrap
    return wrapper