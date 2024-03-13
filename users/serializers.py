from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    # 유저 생성시 UserSerializer 를 사용하기에 
    def create(self, validated_data):
        user = User.objects.create_user(
            email = validated_data["email"],
            password = validated_data["password"],
        )
        return user