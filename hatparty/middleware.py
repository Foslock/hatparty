from .models import HatUser


def user_middleware(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        request.hat_user = HatUser.objects.all()[0]
        response = get_response(request)
        return response

    return middleware
