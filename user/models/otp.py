from django.db import models


class OTP(models.Model):
    phone_number = models.CharField(
        null=True,
        max_length=15,
    )

    code = models.CharField(
        max_length=6,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return self.code
