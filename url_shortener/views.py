from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .models import URL
from .models import AppUser
from utils.url_shortener import generate_short_url, validate_url
from url_shortener_service import settings


def redirect_original(request, short_url):
    url_object = get_object_or_404(URL, short_url=short_url)
    return redirect(url_object.original_url)


def shorten_url(request):
    # Validate the URL
    original_url = request.GET.get('original_url')
    print(original_url)
    user_email = request.GET.get('user_email')
    print(user_email)
    load_balancer_url = getattr(settings, 'MANAGER_URL', "")
    if load_balancer_url == "":
        print("Missing main server url in settings, please check")
        return JsonResponse({'error': f'Invalid server setting'}, status=500)

    if validate_url(original_url):
        short_url = ""
        user, created = AppUser.objects.get_or_create(email=user_email,
                                                      defaults={'name': '', 'creation_date': timezone.now()})
        print("Original URL:", original_url)
        try:
            url = URL.objects.get(original_url=original_url)
            print("Short URL exists:", short_url)
        except URL.DoesNotExist:
            # Generate the short URL
            short_url = generate_short_url(original_url)
            print("Short URL generated:", short_url)

            # Now, let's save the URL to the database
            url = URL.objects.create(short_url=short_url, original_url=original_url, user=user.email)
        return JsonResponse({'short_url': f"{load_balancer_url}/{url.short_url}"})
    else:
        print("Invalid URL")
        return JsonResponse({'error': f'Invalid URL {original_url}'}, status=400)

