from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponsePermanentRedirect
from django.shortcuts import render
from django.views.decorators.http import require_GET


@require_GET
def robots_txt(request):
    robots_path = settings.BASE_DIR / 'static' / 'robots.txt'
    content = robots_path.read_text(encoding='utf-8')
    return HttpResponse(content, content_type='text/plain')


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
