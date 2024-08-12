from django.core.cache import cache
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from user.api.serializers import LoginSerializer


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number')
        ip_address = request.META.get('REMOTE_ADDR')

        # Generate cache keys
        phone_cache_key = f'wrong-login-count-{phone_number}'
        ip_cache_key = f'ip-wrong-login-count-{ip_address}'

        # Get the wrong attempt counts from cache
        wrong_login_count_phone = cache.get(phone_cache_key, 0)
        wrong_login_count_ip = cache.get(ip_cache_key, 0)

        # Check if either the phone number or the IP is blocked
        if wrong_login_count_phone >= 3 or wrong_login_count_ip >= 3:
            return Response({'message': 'You are blocked...'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
            return Response({'results': serializer.validated_data, 'status': status.HTTP_200_OK})

        except Exception as e:
            # Increment the counters for both phone number and IP address
            cache.set(phone_cache_key, wrong_login_count_phone + 1)
            cache.set(ip_cache_key, wrong_login_count_ip + 1)

            # Set the timeout if the max attempts have been reached
            if wrong_login_count_phone + 1 >= 3:
                cache.expire(phone_cache_key, 3600)
            if wrong_login_count_ip + 1 >= 3:
                cache.expire(ip_cache_key, 3600)

            return Response({'message': 'Invalid Username or Password'},
                            status=status.HTTP_400_BAD_REQUEST)
