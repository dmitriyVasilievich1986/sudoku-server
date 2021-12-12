from rest_framework import response, exceptions, status, decorators
from rest_framework.viewsets import GenericViewSet, mixins
from django.contrib.auth.hashers import check_password
from django.shortcuts import get_object_or_404
from django.http.request import HttpRequest
from .serializer import AccountSerializer
from .permissions import TokenPermission
from .models import Account, History
import json


class AccountViewSet(GenericViewSet, mixins.CreateModelMixin):
    permission_classes = [TokenPermission]
    serializer_class = AccountSerializer
    queryset = Account.objects.all()

    def list(self: GenericViewSet, request: HttpRequest, *args: tuple, **kwargs: dict) -> response.Response:
        if request.user is None:
            raise exceptions.NotAuthenticated
        serializer = self.get_serializer(instance=request.user)
        if serializer.is_token_expired:
            raise exceptions.NotAuthenticated
        return response.Response(serializer.data)

    def create(self: GenericViewSet, request: HttpRequest, *args: tuple, **kwargs: dict) -> response.Response:
        serializer: AccountSerializer = self.get_serializer(
            data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED)

    def partial_update(self: GenericViewSet, request: HttpRequest, *args: tuple, **kwargs: dict) -> response.Response:
        instance: Account = self.get_object()
        if request.user is None or instance.id != request.user.id:
            raise exceptions.NotAuthenticated
        instance.update(**request.data)
        serializer: AccountSerializer = self.get_serializer(instance)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED)

    @decorators.action(methods=["POST"], detail=False)
    def login(self: GenericViewSet, request: HttpRequest, *args: tuple, **kwargs: dict) -> response.Response:
        data: dict = json.loads(request.body)
        instance: Account = get_object_or_404(
            klass=Account, username=data.get("username"))
        if not check_password(data.get("password"), instance.password):
            raise exceptions.ValidationError({"password": "wrong password."})
        instance.token_expire = Account.get_token_expire_date()
        instance.token = Account.get_new_token()
        instance.save()
        serializer: AccountSerializer = self.get_serializer(instance)
        return response.Response(serializer.data)

    @decorators.action(methods=["GET"], detail=False)
    def logout(self: GenericViewSet, request: HttpRequest, *args: tuple, **kwargs: dict) -> response.Response:
        instance: Account = request.user
        if instance is None:
            raise exceptions.NotAuthenticated
        instance.logout()
        return response.Response("logout", status.HTTP_204_NO_CONTENT)

    @decorators.action(methods=["POST"], detail=False)
    def history(self: GenericViewSet, request: HttpRequest, *args: tuple, **kwargs: dict) -> response.Response:
        instance: Account = request.user
        data: dict = json.loads(request.body)
        h = History(account=instance, **data)
        h.save()
        serializer = self.get_serializer(instance)
        return response.Response(serializer.data)
