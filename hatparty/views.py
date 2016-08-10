from django.shortcuts import render
from django.views import View


class HomePage(View):
    """ Basic home page
    """
    def get(self, request):
        return render(request, 'home.html', {})
