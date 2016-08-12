from django.shortcuts import render
from django.views import View
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import (
    HttpResponse,
    JsonResponse,
)

from .models import (
    Hat,
    HatUser,
    Like,
    Slap,
    HatTransfer,
    HatSerializer,
    HatUserSerializer,
    LikeSerializer,
    SlapSerializer,
    HatTransferSerializer,
)


class HomePage(View):
    """ Basic home page
    """
    def get(self, request):
        hats = Hat.objects.all()
        users = HatUser.objects.all()
        dct = {
            'hats': hats,
            'users': users,
            'total_counter': sum(u.counter_value for u in users),
        }
        return render(request, 'home.html', dct)


class CreateSlap(APIView):
    """ Slap!
    """
    def post(self, request, user_id=None):
        user = HatUser.objects.get(id=user_id)
        s = Slap(create_user=request.hat_user, target_user=user)
        s.save()
        return Response(SlapSerializer(s).data)


class RefreshDataRoute(APIView):
    """ Returns a giant blob on JSON for loading async data on page
    """
    def get(self, request):
        likes = Like.objects.all()
        slaps = Slap.objects.all()
        transfers = HatTransfer.objects.all()
        hats = Hat.objects.all()
        users = HatUser.objects.all()

        dct = {
            'hats': HatSerializer(hats, many=True).data,
            'users': HatUserSerializer(users, many=True).data,
            'likes': LikeSerializer(likes, many=True).data,
            'slaps': SlapSerializer(slaps, many=True).data,
            'transfers': HatTransferSerializer(transfers, many=True).data,
            'total_counter': sum(u.counter_value for u in users),
        }

        return Response(dct)
