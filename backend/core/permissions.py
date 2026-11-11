from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import User

class IsAdminRole(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and (request.user.is_staff or request.user.role == User.Role.ADMIN))

class RequestObjectPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        return user.is_staff or user.role == User.Role.ADMIN or obj.client_id == user.id or obj.assigned_agent_id == user.id

class OpportunityPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if request.method in SAFE_METHODS:
            return bool(user and user.is_authenticated)
        return bool(user and user.is_authenticated and (user.is_staff or user.role == User.Role.ADMIN))
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return obj.is_published or request.user.role == User.Role.ADMIN or request.user.is_staff
        return request.user.is_staff or request.user.role == User.Role.ADMIN

class ApplicationPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)
    def has_object_permission(self, request, view, obj):
        user = request.user
        return user.is_staff or user.role == User.Role.ADMIN or obj.applicant_id == user.id
