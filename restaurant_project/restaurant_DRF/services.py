from django.contrib.auth.models import Group
from restaurant_app.models import Cart

def manage_user_group(user, group_name, add=True):
    group = Group.objects.get(name=group_name)
    if add:
        user.groups.add(group)
    else:
        user.groups.remove(group)
    user.save()
    
    

    