from rest_framework import serializers, exceptions
from datetime import datetime
from .models import Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            'token_expire',
            'sudoku_cube',
            'dificulty',
            'username',
            'password',
            'history',
            'surname',
            'timer',
            'token',
            'name',
            'help',
            'id',
        ]
        extra_kwargs = {
            'token_expire': {"read_only": True},
            'password': {"write_only": True},
            'history': {"read_only": True},
            'token': {"read_only": True},
            'id': {"read_only": True},
        }

    def create(self: serializers.ModelSerializer, validated_data: dict, *args: tuple, **kwargs: dict) -> Account:
        message: dict = {
            field: "The field cannot be empty"
            for field in ["username", "password"]
            if field not in validated_data
        }
        if message:
            raise exceptions.ValidationError(message)
        instance: Account = Account.create(**validated_data)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        for field in ("name", "surname"):
            instance.__dict__[field] = validated_data[field]
        instance.save()
        return instance

    @property
    def token_expire_date(self: serializers.ModelSerializer, *args: tuple, **kwargs: dict) -> datetime:
        date: datetime = datetime.strptime(
            self.data['token_expire'], "%Y-%m-%dT%H:%M:%S.%fZ")
        return date

    @property
    def is_token_expired(self: serializers.ModelSerializer, *args: tuple, **kwargs: dict) -> bool:
        is_expired: bool = self.token_expire_date < datetime.now()
        return is_expired
