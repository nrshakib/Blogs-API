from rest_framework import permissions

class IsPostAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        safe_methods = ['GET', 'HEAD', 'OPTIONS']
        user = request.user
        author = obj.author

        if request.method in safe_methods:
            return True
        else:
            if user == author:
                return True
            return False