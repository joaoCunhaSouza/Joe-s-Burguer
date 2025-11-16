from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.contrib.auth.decorators import user_passes_test, login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.crypto import get_random_string
from .models import APIToken, OfflineSubmission, Product, Combo
from django.contrib.auth import login
from django.contrib.auth.models import User
import json


def _is_staff(user):
    return user.is_active and (user.is_staff or user.is_superuser)


@user_passes_test(_is_staff)
def generate_token(request):
    """Superuser/staff endpoint to generate a new API token."""
    if request.method == 'POST':
        label = request.POST.get('label', '')
        key = get_random_string(48)
        token = APIToken.objects.create(key=key, label=label, created_by=request.user)
        return JsonResponse({'key': token.key, 'label': token.label})
    return render(request, 'token_generate.html')


@csrf_exempt
def offline_submit(request):
    """Public endpoint clients can POST to with offline data and token key.
    Expected JSON: {"token": "<key>", "payload": {...}}
    """
    if request.method != 'POST':
        return HttpResponseBadRequest('POST required')
    try:
        data = json.loads(request.body.decode('utf-8'))
    except Exception:
        return HttpResponseBadRequest('Invalid JSON')
    token_key = data.get('token')
    payload = data.get('payload')
    if not token_key or payload is None:
        return HttpResponseBadRequest('token and payload required')
    try:
        token = APIToken.objects.get(key=token_key)
    except APIToken.DoesNotExist:
        return HttpResponseForbidden('Invalid token')
    sub = OfflineSubmission.objects.create(token=token, payload=payload)
    return JsonResponse({'status': 'ok', 'id': sub.id})


@login_required
@user_passes_test(_is_staff)
def token_dashboard(request):
    """Dashboard for staff to inspect offline submissions and add items manually.
    A minimal UI: list submissions and a form to create Product/Combo.
    """
    submissions = OfflineSubmission.objects.order_by('-created_at')[:200]
    msg = ''
    if request.method == 'POST':
        # simple handler to create Product or Combo from posted form
        action = request.POST.get('action')
        if action == 'create_product':
            name = request.POST.get('name')
            price = request.POST.get('price') or '0.00'
            description = request.POST.get('description', '')
            if name:
                p = Product.objects.create(name=name, price=price, description=description, image='products/placeholder.png')
                msg = f'Produto {p.name} criado.'
        elif action == 'create_combo':
            name = request.POST.get('name')
            price = request.POST.get('price') or '0.00'
            if name:
                c = Combo.objects.create(name=name, price=price, image='combos/placeholder.png')
                msg = f'Combo {c.name} criado.'
        elif action == 'mark_processed':
            sid = request.POST.get('submission_id')
            try:
                s = OfflineSubmission.objects.get(id=sid)
                s.processed = True
                s.save()
                msg = 'Marked processed.'
            except OfflineSubmission.DoesNotExist:
                msg = 'Submission not found.'
    return render(request, 'token_dashboard.html', {'submissions': submissions, 'message': msg})


@csrf_exempt
def token_login(request):
    """Allow login using token: POST {token: key} will log the corresponding superuser and redirect to dashboard.
    For security the token should be known only to the device.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
        except Exception:
            return HttpResponseBadRequest('Invalid JSON')
        key = data.get('token')
        if not key:
            return HttpResponseBadRequest('token required')
        try:
            token = APIToken.objects.get(key=key)
        except APIToken.DoesNotExist:
            return HttpResponseForbidden('Invalid token')
        # If token has a creator and creator is superuser/staff, login as that user
        user = token.created_by
        if not user or not (user.is_superuser or user.is_staff):
            return HttpResponseForbidden('Token not linked to staff user')
        # Log the user in (session)
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)
        return JsonResponse({'status': 'ok', 'redirect': '/token/dashboard/'})
    # If GET, render a tiny form for manual login
    return render(request, 'token_login.html')
