from django.contrib import admin

from .models import CareLog, Plant


@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    list_display = ("english_name", "biological_name", "count", "status", "planted_on")
    list_filter = ("status", "planted_on")
    search_fields = ("english_name", "biological_name", "local_name", "family_name")


@admin.register(CareLog)
class CareLogAdmin(admin.ModelAdmin):
    list_display = ("plant", "care_type", "performed_on")
    list_filter = ("care_type", "performed_on")

# Register your models here.
