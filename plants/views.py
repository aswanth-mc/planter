from django.contrib import messages
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django.views.generic.base import TemplateView, View

from .forms import CareLogForm, PlantForm
from .models import Plant


class PlantListView(ListView):
    model = Plant
    template_name = "plants/plant_list.html"
    context_object_name = "plants"

    def get_queryset(self):
        show_removed = self.request.GET.get("show_removed") == "1"
        queryset = Plant.objects.all()
        if not show_removed:
            queryset = queryset.filter(status=Plant.Status.ACTIVE)
        return queryset


class PlantDetailView(DetailView):
    model = Plant
    template_name = "plants/plant_detail.html"
    context_object_name = "plant"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["care_form"] = CareLogForm()
        return context


class PlantCreateView(CreateView):
    model = Plant
    form_class = PlantForm
    template_name = "plants/plant_form.html"
    success_url = reverse_lazy("plants:list")

    def form_valid(self, form):
        messages.success(self.request, "Plant added successfully.")
        return super().form_valid(form)


class PlantUpdateView(UpdateView):
    model = Plant
    form_class = PlantForm
    template_name = "plants/plant_form.html"
    success_url = reverse_lazy("plants:list")

    def form_valid(self, form):
        messages.success(self.request, "Plant updated successfully.")
        return super().form_valid(form)


class PlantRemoveView(View):
    def post(self, request, pk):
        plant = get_object_or_404(Plant, pk=pk)
        plant.mark_removed()
        messages.info(request, "Plant marked as removed.")
        return redirect("plants:detail", pk=pk)


class PlantDeleteView(View):
    def post(self, request, pk):
        plant = get_object_or_404(Plant, pk=pk)
        plant.delete()
        messages.warning(request, "Plant permanently deleted.")
        return redirect("plants:list")


class PlantCountAdjustView(View):
    def post(self, request, pk):
        plant = get_object_or_404(Plant, pk=pk)
        action = request.POST.get("action")
        next_url = request.POST.get("next") or reverse("plants:list")

        if action == "increase":
            plant.increase_count()
            messages.success(request, f"{plant.english_name} count increased to {plant.count}.")
        elif action == "decrease":
            previous = plant.count
            plant.decrease_count()
            if plant.count == previous:
                messages.info(request, "Count is already at minimum 1.")
            else:
                messages.success(request, f"{plant.english_name} count reduced to {plant.count}.")
        else:
            messages.error(request, "Invalid count action.")
        return redirect(next_url)


class CareLogCreateView(View):
    def post(self, request, pk):
        plant = get_object_or_404(Plant, pk=pk)
        form = CareLogForm(request.POST)
        if form.is_valid():
            care_log = form.save(commit=False)
            care_log.plant = plant
            care_log.save()
            messages.success(request, "Care activity saved.")
        else:
            messages.error(request, "Unable to save care activity.")
        return HttpResponseRedirect(reverse("plants:detail", kwargs={"pk": pk}))


class DashboardView(TemplateView):
    template_name = "plants/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        start_date = self.request.GET.get("start_date")
        end_date = self.request.GET.get("end_date")
        qs = Plant.objects.all()
        if start_date:
            qs = qs.filter(planted_on__gte=start_date)
        if end_date:
            qs = qs.filter(planted_on__lte=end_date)

        grouped = (
            qs.annotate(day=TruncDate("planted_on"))
            .values("day")
            .annotate(total=Count("id"))
            .order_by("day")
        )
        context["chart_labels"] = [item["day"].isoformat() for item in grouped]
        context["chart_values"] = [item["total"] for item in grouped]
        context["start_date"] = start_date or ""
        context["end_date"] = end_date or ""
        return context
