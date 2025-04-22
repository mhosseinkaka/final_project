from rest_framework import serializers
from user.models import OTP, User

class SendOTPSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=11)

class VerifyOTPSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=11)
    code = serializers.CharField(max_length=10) 