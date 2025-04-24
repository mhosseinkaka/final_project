from django.urls import path
from user.views import UserListView, CreateUserView, UserProfileView, SendOTPView, VerifyOTPView

urlpatterns = [
    path('user-list', UserListView.as_view()),
    path('create-user', CreateUserView.as_view()),
    path('edit-profile/<int:pk>', UserProfileView.as_view()),
    path('send-otp/', SendOTPView.as_view()),
    path('verify-otp/', VerifyOTPView.as_view()),
]