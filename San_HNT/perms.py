

from rest_framework import permissions
from rest_framework.permissions import BasePermission


class OwnerPerms(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        print(f"User: {type(request.user)} ")
        return super().has_object_permission(request, view, obj) and request.user.id == int(view.kwargs.get('pk'))
# class OwnerPermsToSupplier(OwnerPerms):
#     def has_object_permission(self, request, view, obj):
#         return super().has_object_permission(request, view, obj) and request.supplier == obj



class IsUserSelf(BasePermission):
    def has_permission(self, request, view):
        print(f"User: {type(request.user.id)} ")
        print(type(view.kwargs.get('pk')))
        return request.user.id == view.kwargs.get('pk')