from django.contrib.auth.models import AnonymousUser
from rest_framework.permissions import BasePermission
from rest_framework import permissions
from .models import *


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)


class IsAdminOrCarOwnerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return True
        user = request.user
        return user.is_authenticated and (user.is_staff or CarOwner.objects.filter(user=user).exists())


class IsAdminOrDealerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return True
        user = request.user
        return user.is_staff or Dealer.objects.filter(user=user).exists()
