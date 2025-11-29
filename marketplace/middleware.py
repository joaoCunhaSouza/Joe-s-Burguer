from django.conf import settings
from django.http import HttpResponseForbidden


class KitchenIPRestrictionMiddleware:
    """Block access to /kitchen... routes unless the client IP is allowed.

    The allowed IPs are read from settings.KITCHEN_ALLOWED_IPS (list of strings).
    If the setting is empty or not defined, the middleware does nothing.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.allowed = set(getattr(settings, 'KITCHEN_ALLOWED_IPS', []) or [])

    def __call__(self, request):
        path = (request.path or '').lower()
        if path.startswith('/kitchen') and self.allowed:
            # Prefer X-Forwarded-For (first entry) when behind a proxy
            xff = request.META.get('HTTP_X_FORWARDED_FOR')
            if xff:
                client_ip = xff.split(',')[0].strip()
            else:
                client_ip = request.META.get('REMOTE_ADDR')

            if client_ip not in self.allowed:
                return HttpResponseForbidden('Acesso proibido')

        return self.get_response(request)
