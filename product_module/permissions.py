from rest_framework import permissions

class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        print("User:", request.user)
        print("Authenticated:", request.user.is_authenticated)
        print("Is manager:", request.user.groups.filter(name='manager').exists())
        return (
            request.user
            and request.user.is_authenticated
            and request.user.groups.filter(name='manager').exists()
        )

class IsUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.groups.filter(name='user').exists()
        )

class IsPublic(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.groups.filter(name='public').exists()
        )

class CanViewProduct(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and (
                request.user.groups.filter(name='manager').exists()
                or request.user.groups.filter(name='user').exists()
                or request.user.groups.filter(name='public').exists()
            )
        )

