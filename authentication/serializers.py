from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')

        if not username.isalnum():
            raise serializers.ValidationError('The username should onlycontain alphanumeric character')
        return attrs

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ['token']


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=555)
    password = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ['username', 'password']
