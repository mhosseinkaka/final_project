from rest_framework.serializers import ModelSerializer, StringRelatedField
from user.models import User
from rest_framework import serializers

class UserProfileSerializer(ModelSerializer):
    phone = StringRelatedField()
    first_name = StringRelatedField()
    last_name = StringRelatedField()
    role = StringRelatedField()
    class Meta:
        model = User
        fields = ['phone', 'first_name', 'last_name', 'role']
        read_only_fields = ['phone', 'role']

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserListSerializer(ModelSerializer):
    phone = StringRelatedField()
    first_name = StringRelatedField()
    last_name = StringRelatedField()
    role = StringRelatedField()
    class Meta:
        model = User
        fields = ['phone', 'first_name', 'last_name', 'role', 'is_active', 'is_staff']
        read_only_fields = ['phone', 'role']


class SendOTPSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=11)

class VerifyOTPSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=11)
    code = serializers.CharField(max_length=6)