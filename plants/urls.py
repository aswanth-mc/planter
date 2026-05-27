from django.urls import path

from .views import (
    CareLogCreateView,
    DashboardView,
    PlantCountAdjustView,
    PlantCreateView,
    PlantDeleteView,
    PlantDetailView,
    PlantListView,
    PlantRemoveView,
    PlantUpdateView,
)

app_name = "plants"

urlpatterns = [
    path("", PlantListView.as_view(), name="list"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("new/", PlantCreateView.as_view(), name="create"),
    path("<int:pk>/", PlantDetailView.as_view(), name="detail"),
    path("<int:pk>/edit/", PlantUpdateView.as_view(), name="update"),
    path("<int:pk>/remove/", PlantRemoveView.as_view(), name="remove"),
    path("<int:pk>/delete/", PlantDeleteView.as_view(), name="delete"),
    path("<int:pk>/count/", PlantCountAdjustView.as_view(), name="count-adjust"),
    path("<int:pk>/care/", CareLogCreateView.as_view(), name="care-add"),
]
