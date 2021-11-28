from rest_framework.permissions import BasePermission
from django.http import HttpRequest
from datetime import datetime
from .models import Account
from typing import Union
import re


class TokenPermission(BasePermission):
    def has_permission(self: BasePermission, request: HttpRequest, *args: tuple, **kwargs: dict) -> bool:
        token: str = request.META.get("HTTP_AUTHORIZATION")
        user: Union[None, Account] = None
        if token is not None and re.match(r'token ', token):
            token = re.sub(r'^token ', "", token)
            user = Account.objects.filter(token=token)
            user = user[0] if user.count() > 0 else None
        request.user = user
        return True
