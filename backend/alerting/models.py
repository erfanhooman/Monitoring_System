from django.db import models
from settings.models import UserSystem

class UserAlertPreference(models.Model):
    user = models.ForeignKey(UserSystem, on_delete=models.CASCADE, related_name='alert_preferences')
    item_key = models.CharField(max_length=255)
    enabled = models.BooleanField(default=False)
    alert_level = models.CharField(
        max_length=10,
        choices=[('warning', 'Warning'), ('critical', 'Critical')],
        default='critical'
    )

    class Meta:
        unique_together = ('user', 'item_key')

    def __str__(self):
        return f"{self.user} - {self.item_key} - {self.enabled}"
