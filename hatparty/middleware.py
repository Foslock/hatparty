from .models import HatUser
from django.http import HttpResponseRedirect

LOGIN_PATH = "/login/"


def user_middleware(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        if not request.path.startswith("/admin"):
            auth_key = request.session.get('user_auth_token')
            if auth_key:
                user = HatUser.objects.filter(
                    auth_token=auth_key).first()
                if user:
                    request.hat_user = user
                    response = get_response(request)
                    return response

            if request.path != LOGIN_PATH:
                return HttpResponseRedirect(LOGIN_PATH)
            else:
                return get_response(request)

        return get_response(request)

    return middleware
