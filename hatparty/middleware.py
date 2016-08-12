from .models import HatUser


def user_middleware(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        users = HatUser.objects.all()
        if users:
            request.hat_user = users[0]
        response = get_response(request)
        return response

    return middleware
