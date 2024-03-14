from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import Token

from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    # 유저 생성시 UserSerializer 를 사용하기에 
    def create(self, validated_data):
        if validated_data["nickname"]:
            user = User.objects.create_user(
                email = validated_data["email"],
                password = validated_data["password"],
                nickname = validated_data["nickname"]
            )
            return user
        user = User.objects.create_user(
            email = validated_data["email"],
            password = validated_data["password"]
        )
        return user


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user: User) -> Token:
        token = super().get_token(user)

        token['email'] = user.email

        return token