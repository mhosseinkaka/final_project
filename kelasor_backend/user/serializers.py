from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, StringRelatedField
from user.models import OTP, User

class UserProfileSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['phone', 'first_name', 'last_name', 'role']
        read_only_fields = ['phone', 'role']

class SendOTPSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=11)

class VerifyOTPSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=11)
    code = serializers.CharField(max_length=10) 