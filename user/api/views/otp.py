from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from user.api.serializers import OTPSerializer, CheckOTPSerializer
from user.models import OTP, User
from django.core.cache import cache


class OTPView(CreateAPIView):
    serializer_class = OTPSerializer
    permission_classes = []


class CheckOTPView(CreateAPIView):
    serializer_class = CheckOTPSerializer
    permission_classes = []

    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number')
        ip_address = request.META.get('REMOTE_ADDR')

        # Generate cache keys
        phone_cache_key = f'wrong-otp-count-{phone_number}'
        ip_cache_key = f'ip-wrong-otp-count-{ip_address}'

        # Get the wrong attempt counts from cache
        wrong_otp_count_phone = cache.get(phone_cache_key, 0)
        wrong_otp_count_ip = cache.get(ip_cache_key, 0)

        # Check if either the phone number or the IP is blocked
        if wrong_otp_count_phone >= 3 or wrong_otp_count_ip >= 3:
            return Response({'message': 'You are blocked...'}, status=status.HTTP_400_BAD_REQUEST)

        code = request.data.get('code')
        # Check if the OTP is correct
        if OTP.objects.filter(code=code, phone_number=phone_number).exists():
            return Response(status=status.HTTP_200_OK)

        # Increment the counters for both phone number and IP address
        cache.set(phone_cache_key, wrong_otp_count_phone + 1)
        cache.set(ip_cache_key, wrong_otp_count_ip + 1)

        # Set the timeout if the max attempts have been reached
        if wrong_otp_count_phone + 1 >= 3:
            cache.expire(phone_cache_key, 3600)
        if wrong_otp_count_ip + 1 >= 3:
            cache.expire(ip_cache_key, 3600)

        return Response({'message': 'OTP did not match...'},
                        status=status.HTTP_400_BAD_REQUEST)
