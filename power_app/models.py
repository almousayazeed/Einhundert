from django.db import models

class PowerData(models.Model):
    timestamp = models.DateTimeField()
    current = models.FloatField()
    voltage = models.FloatField()
    power = models.FloatField(editable=False)  # Power will be calculated automatically

    def save(self, *args, **kwargs):
        self.power = self.current * self.voltage  # Calculate power
        super().save(*args, **kwargs)

    class Meta:
        indexes = [
            models.Index(fields=['timestamp']),  # Index on timestamp for faster filtering
        ]