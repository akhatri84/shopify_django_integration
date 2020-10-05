from django.shortcuts import render, redirect, HttpResponse
import shopify
from django.contrib import messages
from django.urls import reverse
import binascii, os
from django.apps import apps


# Create your views here.

def _new_session(shop_url):
    api_version = apps.get_app_config('shopify_app').SHOPIFY_API_VERSION
    return shopify.Session(shop_url, api_version)


def login(request):
    if request.GET.get('shop'):
        return authenticate(request)
    return render(request, 'shopify/login.html', {})


def authenticate(request):
    shop_url = request.GET.get('shop', request.POST.get('shop')).strip()

    if not shop_url:
        messages.error(request, "A shop param is required")
        return redirect(reverse(login))
    #    scope = apps.get_app_config('shopify').SHOPIFY_API_SCOPE
    redirect_uri = request.build_absolute_uri(reverse(finalize))
    state = binascii.b2a_hex(os.urandom(15)).decode("utf-8")
    request.session['shopify_oauth_state_param'] = state
    #    permission_url = _new_session(shop_url).create_permission_url(scope, redirect_uri, state)
    return redirect(permission_url)


def test1(request):
    API_KEY = '8f7b8feb368351f9cac89d57244822ca'
    SHARED_SECRET = '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'

    shop_url = "https://%s:%s@redfeetbrothers.myshopify.com" % (API_KEY, SHARED_SECRET)
    api_version = '2020-01'
    state = binascii.b2a_hex(os.urandom(15)).decode("utf-8")
    redirect_uri = "http://localhost:8000/data/"
    scopes = ['read_products', 'read_orders']

    newSession = shopify.Session(shop_url, api_version)
    auth_url = newSession.create_permission_url(scopes, redirect_uri, state)
    return redirect(to=auth_url)
    # return HttpResponse("Akash")


def test(request):
    API_KEY = '8f7b8feb368351f9cac89d57244822ca'
    SHARED_SECRET = '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'

    shopify.Session.setup(api_key=API_KEY, secret=SHARED_SECRET)
    shop_url = "redfeetbrothers.myshopify.com"
    api_version = '2020-01'
    state = binascii.b2a_hex(os.urandom(15)).decode("utf-8")
    redirect_uri = "localhost:8000/data/"
    scopes = ['read_products', 'read_orders']

    newSession = shopify.Session(shop_url, api_version)
    auth_url = newSession.create_permission_url(scopes, redirect_uri, state)

    return redirect(to=auth_url)

def getdata(request):
    print(request)
    return HttpResponse("Khatri")
