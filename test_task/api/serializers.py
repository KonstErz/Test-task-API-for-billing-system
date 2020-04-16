from rest_framework import serializers
from django.contrib.auth.models import User


class RegistrationSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate_email(self, attr):
        if User.objects.filter(email=attr).exists():
            raise serializers.ValidationError('email already exist')

        return attr

    def validate_username(self, attr):
        if User.objects.filter(username=attr).exists():
            raise serializers.ValidationError('username already exist')

        return attr


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

