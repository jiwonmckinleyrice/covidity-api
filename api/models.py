from django.db import models


class District(models.Model):
    name = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)


class ConfirmedCase(models.Model):
    district = models.ForeignKey(
        District, related_name="confirmed_cases", on_delete=models.CASCADE)
    count = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
