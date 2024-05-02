from rest_framework.permissions import BasePermission


class MenuItemPermittions(BasePermission):
    
    allowed_groups_for_post = ['Manager','Admin','Editor']
    
    def has_permission(self, request, view):
        
        # Check for authenticated user
        if not request.user.is_authenticated:
            return False
        # Deny everything that is not GET or POST
        if request.method not in ['GET','POST'] :
            return False
        # Check if User has permittions for POST (Manager Role)
        if request.method == 'POST':
            return request.user.groups.filter(name='Manager').exists()
        return True
    
    
class SpecificMenuItemPermittions(BasePermission):
    
    allowed_groups_for_post = ['Manager','Admin','Editor']
    
    def has_permission(self, request, view):
        
        # Check for authenticated user
        if not request.user.is_authenticated:
            return False
        # Deny everything that is not GET or POST
        if request.method not in ['GET','PUT','PATCH','DELETE'] :
            return False
        # Check if User has permittions for PUT and PATCH (Manager Role)
        if request.method in ['PUT','PATCH','DELETE']:
            return request.user.groups.filter(name='Manager').exists()
        return True