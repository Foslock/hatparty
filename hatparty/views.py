from django.shortcuts import render
from django.views import View
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import (
    HttpResponse,
    JsonResponse,
    HttpResponseRedirect,
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
        hat_transfers = HatTransfer.objects.order_by("-create_date")[:50]
        dct = {
            'hats': hats,
            'users': users,
            'total_counter': sum(u.counter_value for u in users),
            'hat_user': request.hat_user,
            'hat_transfers': hat_transfers,
        }
        return render(request, 'home.html', dct)


class HatUserCreate(View):
    """ Un-auth'd page to create user
    """
    def get(self, request):
        return render(request, 'login.html', {})

    def post(self, request):
        name = request.POST.get('name')
        email = request.POST.get('email')
        matching_user = HatUser.objects.filter(name=name).first()
        if matching_user:
            user = matching_user
        else:
            user = HatUser()
            user.name = name
        if email:
            user.email = email
        user.save()
        request.session['user_auth_token'] = str(user.auth_token)
        return HttpResponseRedirect("/")


class CreateSlap(APIView):
    """ Slap!
    """
    def post(self, request, user_id=None):
        user = HatUser.objects.get(id=user_id)
        s = Slap(create_user=request.hat_user, target_user=user)
        s.save()
        return Response(SlapSerializer(s).data)


class ClaimHatRoute(APIView):
    """
    """
    def post(self, request, hat_id=None):
        hat = Hat.objects.get(id=hat_id)
        if hat:
            transfer = HatTransfer()
            if hat.current_wearer:
                transfer.source_user = hat.current_wearer
            transfer.target_user = request.hat_user
            transfer.hat = hat
            transfer.save()
            request.hat_user.current_hat = hat
            request.hat_user.save()
        return Response()


class DitchHatRoute(APIView):
    """
    """
    def post(self, request, hat_id=None):
        hat = Hat.objects.get(id=hat_id)
        if hat and hat.current_wearer:
            transfer = HatTransfer()
            transfer.source_user = request.hat_user
            transfer.target_user = None
            transfer.hat = hat
            transfer.save()
            request.hat_user.current_hat = None
            request.hat_user.save()
        return Response()


class LikeHatRoute(APIView):
    """
    """
    def post(self, request, hat_id=None):
        hat = Hat.objects.get(id=hat_id)
        if hat and hat.current_wearer:
            like = Like()
            like.create_user = request.hat_user
            like.target_user = hat.current_wearer
            like.hat = hat
            like.save()
        return Response()


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


class IncrementCounter(APIView):
    """ Hehe
    """
    def post(self, request):
        request.hat_user.counter_value += 1
        request.hat_user.save()
        return Response()
