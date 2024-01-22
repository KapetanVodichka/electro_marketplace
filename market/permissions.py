from rest_framework import permissions


class IsActiveAndStaff(permissions.BasePermission):
    """
    Кастомное разрешение для доступа только активных сотрудников.
    """

    def has_permission(self, request, view):
        return request.user.is_active and request.user.is_staff