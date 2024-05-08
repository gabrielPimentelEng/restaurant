from rest_framework.throttling import SimpleRateThrottle

class AuthenticatedUserThrottle(SimpleRateThrottle):
    scope = 'authenticated_user'

    def get_cache_key(self, request, view):
        if request.user.is_authenticated:
            ident = request.user.pk
            return f'{self.scope}:{ident}'
        return None
    
class UnauthenticatedUserThrottle(SimpleRateThrottle):
    scope = 'unauthenticated_user'

    def get_cache_key(self, request, view):
        if not request.user.is_authenticated:
            ident = self.get_ident(request) # Typically the user's IP address
            return f'{self.scope}:{ident}'
        return None