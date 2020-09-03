from django.db import models


class District(models.Model):
    name = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ConfirmedCase(models.Model):
    district = models.ForeignKey(
        District, related_name="confirmed_cases", on_delete=models.CASCADE)
    count = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
