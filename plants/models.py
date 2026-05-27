from django.db import models
from django.utils import timezone


class Plant(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        REMOVED = "removed", "Removed"

    biological_name = models.CharField(max_length=200)
    local_name = models.CharField(max_length=200, blank=True)
    english_name = models.CharField(max_length=200)
    family_name = models.CharField(max_length=200, blank=True)
    care_notes = models.TextField(blank=True)
    image = models.ImageField(upload_to="plants/", blank=True, null=True)
    count = models.PositiveIntegerField(default=1)
    planted_on = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
    )
    removed_on = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-planted_on", "-created_at"]

    def __str__(self):
        return f"{self.english_name} ({self.biological_name})"

    def mark_removed(self):
        self.status = self.Status.REMOVED
        self.removed_on = timezone.localdate()
        self.save(update_fields=["status", "removed_on", "updated_at"])

    def increase_count(self, amount=1):
        self.count += amount
        self.save(update_fields=["count", "updated_at"])

    def decrease_count(self, amount=1):
        self.count = max(1, self.count - amount)
        self.save(update_fields=["count", "updated_at"])


class CareLog(models.Model):
    class CareType(models.TextChoices):
        WATERING = "watering", "Watering"
        FERTILIZER = "fertilizer", "Fertilizer"
        PRUNING = "pruning", "Pruning"
        REPOTTING = "repotting", "Repotting"
        OTHER = "other", "Other"

    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name="care_logs")
    care_type = models.CharField(max_length=20, choices=CareType.choices)
    notes = models.TextField(blank=True)
    performed_on = models.DateField(default=timezone.localdate)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-performed_on", "-created_at"]

    def __str__(self):
        return f"{self.get_care_type_display()} for {self.plant.english_name}"
