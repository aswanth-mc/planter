from django import forms

from .models import CareLog, Plant


class PlantForm(forms.ModelForm):
    class Meta:
        model = Plant
        fields = [
            "biological_name",
            "local_name",
            "english_name",
            "family_name",
            "care_notes",
            "image",
            "count",
            "planted_on",
            "status",
        ]
        widgets = {
            "planted_on": forms.DateInput(attrs={"type": "date"}),
            "care_notes": forms.Textarea(attrs={"rows": 4}),
            "count": forms.NumberInput(attrs={"min": 1}),
        }


class CareLogForm(forms.ModelForm):
    class Meta:
        model = CareLog
        fields = ["care_type", "notes", "performed_on"]
        widgets = {
            "performed_on": forms.DateInput(attrs={"type": "date"}),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }
