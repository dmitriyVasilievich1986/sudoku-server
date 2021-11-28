from datetime import datetime, timedelta
from django.utils import timezone
from django.db import models
from typing import Any, Union
from uuid import uuid4


class Account(models.Model):
    username: models.CharField = models.CharField(
        max_length=50, unique=True, null=False, blank=False)
    name: models.CharField = models.CharField(
        max_length=50, unique=False, null=True, blank=True)
    surname: models.CharField = models.CharField(
        max_length=50, unique=False, null=True, blank=True)
    token: models.CharField = models.CharField(
        max_length=50, unique=True, null=False, blank=False)
    token_expire: models.DateTimeField = models.DateTimeField(
        blank=False, null=False)

    @classmethod
    def create(
        cls: models.Model,
        username: str,
        name: Union[None, str] = None,
        surname: Union[None, str] = None,
        *args: tuple,
        **kwargs: dict
    ) -> models.Model:
        token: str = cls.get_new_token()
        token_expire: datetime = cls.get_token_expire_date()
        return cls(username=username, name=name, surname=surname, token=token, token_expire=token_expire)

    @classmethod
    def get_new_token(cls: models.Model, *args: tuple, **kwargs: dict) -> str:
        token: Union[None, str] = None
        while token is None:
            token = str(uuid4())
            is_exists: bool = cls.objects.filter(
                token=token).count() > 0
            token = None if is_exists else token
        return token

    @staticmethod
    def get_token_expire_date(*args: tuple, **kwargs: dict):
        token_expired: datetime = timezone.now() + timedelta(days=1)
        return token_expired

    def is_same_token(self: models.Model, token: str, *args: tuple, **kwargs: dict) -> bool:
        instance_token: str = f"token {self.token}"
        is_same: bool = instance_token == token
        return is_same

    def __getitem__(self: models.Model, value: str, *args: tuple, **kwargs: dict) -> Any:
        return self.__dict__[value]

    def update(self: models.Model, *args: tuple, **kwargs: dict) -> models.Model:
        self.name = kwargs.get("name", self["name"])
        self.surname = kwargs.get("surname", self["surname"])
        self.save()
        return self

    def logout(self: models.Model, *args: tuple, **kwargs: dict) -> None:
        self.token_expire = timezone.now()
        self.save()
