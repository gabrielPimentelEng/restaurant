from rest_framework.permissions import BasePermission
from django.db.models import Q


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
        elif request.method != 'DELETE':
            return False
        else :
            return request.user.groups.filter(name='Manager').exists()
        
class CartManagementPermissions(BasePermission):
    
    def has_permission(self, request,view):
        
        # Check for authenticated user
        if not request.user.is_authenticated:
            return False
        # Check if User has permittions for POST (Manager Role)
        # Deny everything that is not GET, POST or DELETE
        elif request.method not in ['GET','POST','DELETE'] :
            return False
        else:
            return not request.user.groups.exists()
    
class OrderPermissions(BasePermission):

    def has_permission(self, request,view):

        # Check for authenticated user
        if not request.user.is_authenticated:
            return False
        # For POST only users that does not have group  
        if request.method == 'POST'  :
            return not request.user.groups.exists()
        
        elif request.method in ['PUT','PATCH','DELETE']:
    
            # For PATCH, check if the user is in 'Delivery Crew' or 'Manager'
            # For PUT, check if the user is in 'Manager' only
            # Filter based if is PUT or PATCH
            required_groups = ['Manager'] if request.method in ['PUT','DELETE'] else ['Delivery Crew','Manager']
            user_in_required_groups = request.user.groups.filter(name__in=required_groups).exists()
            return user_in_required_groups

        return True

