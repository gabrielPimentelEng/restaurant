from rest_framework.permissions import BasePermission


class MenuItemPermittions(BasePermission):
    
    def has_permission(self, request, view):
        
        # Check for authenticated user
        if not request.user.is_authenticated:
            return False
        # Deny everything that is not GET or POST
        elif request.method not in ['GET','POST'] :
            return False
        # Check if User has permittions for POST (Manager Role)
        elif request.method == 'POST':
            return request.user.groups.filter(name='Manager').exists()
        return True
    
    
class SpecificMenuItemPermittions(BasePermission):
    
    allowed_groups_for_post = ['Manager','Admin','Editor']
    
    def has_permission(self, request, view):
        
        # Check for authenticated user
        if not request.user.is_authenticated:
            return False
        # Deny everything that is not GET or POST
        elif request.method not in ['GET','PUT','PATCH','DELETE'] :
            return False
        # Check if User has permittions for PUT, PATCH and DELETE (Manager Role)
        if request.method in ['PUT','PATCH','DELETE']:
            return request.user.groups.filter(name='Manager').exists()
        return True
    
class GroupManagementPermittions(BasePermission):
    
    def has_permission(self, request,view):
        
        # Check for authenticated user
        if not request.user.is_authenticated:
            return False
        # Deny everything that is not GET or POST
        elif request.method not in ['GET','POST'] :
            return False
        # Check if User has permittions for GET and POST (Manager Role)
        else :
            return request.user.groups.filter(name='Manager').exists()
        
class DeleteUserFromGroupPermittions(BasePermission):
    
    def has_permission(self, request,view):
        
        # Check for authenticated user
        if not request.user.is_authenticated:
            return False
        # Check if User has permittions for POST (Manager Role)
        else :
            return request.user.groups.filter(name='Manager').exists()
 