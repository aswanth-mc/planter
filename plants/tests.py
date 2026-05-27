from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import CareLog, Plant


class PlantModelTests(TestCase):
    def test_default_count_is_one(self):
        plant = Plant.objects.create(
            biological_name="Mentha spicata",
            english_name="Mint",
            planted_on=timezone.localdate(),
        )
        self.assertEqual(plant.count, 1)

    def test_mark_removed_sets_status_and_date(self):
        plant = Plant.objects.create(
            biological_name="Ocimum tenuiflorum",
            local_name="Tulsi",
            english_name="Holy Basil",
            planted_on=timezone.localdate(),
        )

        plant.mark_removed()
        plant.refresh_from_db()

        self.assertEqual(plant.status, Plant.Status.REMOVED)
        self.assertIsNotNone(plant.removed_on)


class PlantViewsTests(TestCase):
    def setUp(self):
        self.plant = Plant.objects.create(
            biological_name="Aloe vera",
            local_name="Ghritkumari",
            english_name="Aloe Vera",
            planted_on=timezone.localdate(),
        )

    def test_list_page_loads(self):
        response = self.client.get(reverse("plants:list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Aloe Vera")

    def test_add_care_log(self):
        response = self.client.post(
            reverse("plants:care-add", kwargs={"pk": self.plant.pk}),
            {
                "care_type": CareLog.CareType.WATERING,
                "notes": "Evening watering",
                "performed_on": timezone.localdate(),
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.plant.care_logs.count(), 1)

    def test_remove_plant(self):
        response = self.client.post(reverse("plants:remove", kwargs={"pk": self.plant.pk}))
        self.assertEqual(response.status_code, 302)
        self.plant.refresh_from_db()
        self.assertEqual(self.plant.status, Plant.Status.REMOVED)

    def test_count_adjust_buttons(self):
        increase_response = self.client.post(
            reverse("plants:count-adjust", kwargs={"pk": self.plant.pk}),
            {"action": "increase", "next": reverse("plants:list")},
        )
        self.assertEqual(increase_response.status_code, 302)
        self.plant.refresh_from_db()
        self.assertEqual(self.plant.count, 2)

        decrease_response = self.client.post(
            reverse("plants:count-adjust", kwargs={"pk": self.plant.pk}),
            {"action": "decrease", "next": reverse("plants:list")},
        )
        self.assertEqual(decrease_response.status_code, 302)
        self.plant.refresh_from_db()
        self.assertEqual(self.plant.count, 1)
