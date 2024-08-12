from rest_framework.generics import CreateAPIView

from user.api.serializers import SignupSerializer


class SignupView(CreateAPIView):
    serializer_class = SignupSerializer
    permission_classes = []
