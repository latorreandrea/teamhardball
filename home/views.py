from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponsePermanentRedirect
from django.shortcuts import render


def index(request):
    return render(request, 'home/index.html')


def contact(request):
    return render(request, 'home/contact.html')


def privacy_policy(request):
    return render(request, 'home/privacy_policy.html')


def discord_redirect(request):
    return HttpResponsePermanentRedirect(settings.DISCORD_URL)


@login_required
def hq(request):
    return render(request, 'home/hq.html')
