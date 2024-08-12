import random
from rest_framework import serializers
from user.models import OTP


class OTPSerializer(serializers.ModelSerializer):
    code = serializers.CharField(read_only=True)

    class Meta:
        model = OTP
        fields = ['phone_number', 'code']

    def create(self, validated_data):
        otp_code = str(random.randint(100000, 999999))
        phone_number = validated_data.get('phone_number')
        otp = OTP.objects.filter(phone_number=phone_number).first()
        if otp:
            otp.code = otp_code
            otp.save()
            return otp
        return OTP.objects.create(**validated_data, code=otp_code)


class CheckOTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTP
        fields = ['phone_number', 'code']
