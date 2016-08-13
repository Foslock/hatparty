from .models import HatUser
from django.http import HttpResponseRedirect


def user_middleware(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        auth_key = request.session.get('user_auth_token')
        if auth_key:
            request.hat_user = HatUser.objects.filter(
                auth_token=auth_key).first()
            response = get_response(request)
            return response
        elif request.path != "/login/":
            return HttpResponseRedirect("/login/")
        else:
            return get_response(request)

    return middleware
