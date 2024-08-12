from django.urls import path
from rest_framework.routers import DefaultRouter

from user.api.views import LoginView, SignupView, OTPView, CheckOTPView

router = DefaultRouter()
router.register(r'otp', OTPView, basename='otp')


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('otp/', OTPView.as_view(), name='otp'),
    path('check_otp/', CheckOTPView.as_view(), name='check-otp'),

]

