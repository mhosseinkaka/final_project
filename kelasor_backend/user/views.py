from django.http.response import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView 
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from user.models import User, OTP
from user.serializers import UserSerializer, UserProfileSerializer, UserListSerializer, SendOTPSerializer, VerifyOTPSerializer
from user.permissions import IsSuperUser, IsSupport
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
import random
from django.utils import timezone
from datetime import timedelta
from rest_framework_simplejwt.tokens import RefreshToken
from user.tasks import send_otp_task


# Create your views here.

class UserListView(ListAPIView):
    permission_classes = [IsSuperUser and IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['last_name', 'first_name', 'role', 'is_active']
    search_fields = ['role']
    
class CreateUserView(CreateAPIView):
    permission_classes = [IsSuperUser and IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserProfileView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer

class SendOTPView(APIView):
    def post(self, request):
        serializer = SendOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone']

        recent = OTP.objects.filter(phone=phone).order_by('-created_at').first()
        if recent and recent.created_at > timezone.now() - timedelta(seconds=90):
            return Response({"detail": "کد اخیراً ارسال شده، لطفاً کمی صبر کنید."}, status=429)

        code = str(random.randint(100000, 999999))
        OTP.objects.create(phone=phone, code=code)

        send_otp_task.delay(phone, code)

        return Response({"detail": "کد تأیید ارسال شد."})


class VerifyOTPView(APIView):
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone']
        code = serializer.validated_data['code']

        otp_qs = OTP.objects.filter(phone=phone, code=code).order_by('-created_at')
        if not otp_qs.exists() or not otp_qs.first().is_valid():
            return Response({"detail": "کد اشتباه یا منقضی شده."}, status=400)

        user, created = User.objects.get_or_create(phone=phone)

        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'is_new_user': created
        })