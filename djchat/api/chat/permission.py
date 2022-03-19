from rest_framework import permissions

from .logics import is_exists_chat


class IsChatUserAndIsAuthenticatedRetrive(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        return is_exists_chat(request.user, obj.id)


class IsChatUserAndIsAuthenticatedList(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        room_id = request.parser_context['kwargs']['pk']
        return is_exists_chat(request.user, room_id)
        