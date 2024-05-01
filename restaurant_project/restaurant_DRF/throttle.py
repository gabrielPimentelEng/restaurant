from rest_framework.throttling import SimpleRateThrottle

class CustomRateThrottle(SimpleRateThrottle):
    scope = 'custom'

    def get_cache_key(self, request, view):
        if request.user.is_authenticated:
            ident = request.user.pk
        else:
            ident = self.get_ident(request)
        return f'{self.scope}:{ident}'