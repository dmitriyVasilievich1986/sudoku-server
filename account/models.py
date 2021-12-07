from django.contrib.auth.hashers import make_password
from datetime import datetime, timedelta
from django.utils import timezone
from typing import Any, Union
from django.db import models
from os import environ
from uuid import uuid4


class Account(models.Model):
    username: models.CharField = models.CharField(
        max_length=50, unique=True, null=False, blank=False)
    password: models.CharField = models.CharField(
        max_length=150, unique=False, null=False, blank=False)
    name: models.CharField = models.CharField(
        max_length=50, unique=False, null=True, blank=True)
    surname: models.CharField = models.CharField(
        max_length=50, unique=False, null=True, blank=True)
    sudoku_cube: models.TextField = models.TextField(
        unique=False, null=True, blank=True)
    token: models.CharField = models.CharField(
        max_length=50, unique=True, null=False, blank=False)
    token_expire: models.DateTimeField = models.DateTimeField(
        blank=False, null=False)
    dificulty: models.IntegerField = models.IntegerField(default=40)
    help: models.BooleanField = models.BooleanField(default=True)

    @classmethod
    def create(
        cls: models.Model,
        username: str,
        password: str,
        name: Union[None, str] = None,
        surname: Union[None, str] = None,
        *args: tuple,
        **kwargs: dict
    ) -> models.Model:
        hashed_password = make_password(
            password=password, salt=environ.get("SALT", "salt"))
        token: str = cls.get_new_token()
        token_expire: datetime = cls.get_token_expire_date()
        return cls(username=username, name=name, surname=surname, token=token, token_expire=token_expire, password=hashed_password)

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
        self.sudoku_cube = kwargs.get("sudoku_cube", self["sudoku_cube"])
        self.dificulty = kwargs.get("dificulty", self["dificulty"])
        self.surname = kwargs.get("surname", self["surname"])
        self.help = kwargs.get("help", self["help"])
        self.name = kwargs.get("name", self["name"])
        self.save()
        return self

    def logout(self: models.Model, *args: tuple, **kwargs: dict) -> None:
        self.token_expire = timezone.now()
        self.save()
