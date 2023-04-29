from rest_framework import permissions


class ReadAndOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (obj.author == request.user
                or request.method in permissions.SAFE_METHODS)
# В сравнении с предыдущим спринтом добавил ток Safe_Methods
# Чтобы получать GET с noauth пользователем
