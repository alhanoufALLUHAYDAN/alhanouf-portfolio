from django.db import models
import uuid
# Create your models here.


class Visitor(models.Model):
    device_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    ip_address = models.GenericIPAddressField()
    browser = models.CharField(max_length=100, null=True, blank=True)
    os = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_seen = models.DateTimeField(auto_now=True)
    visit_count = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.ip_address} - {self.country or 'Unknown'}"

class VisitLog(models.Model):
    visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE, related_name='logs')
    page_url = models.CharField(max_length=255)
    referrer = models.URLField(null=True, blank=True) #
    entry_time = models.DateTimeField(auto_now_add=True)
    exit_time = models.DateTimeField(null=True, blank=True)
    duration_seconds = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Visit to {self.page_url} at {self.entry_time}"