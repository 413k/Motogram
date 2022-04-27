from django.views import generic as views
from django.shortcuts import redirect

from motogram.common.view_mixins import RedirectToDashboard
from motogram.main.models import VehiclePhoto


class HomeView(RedirectToDashboard, views.TemplateView):
    template_name = 'main/home_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hide_additional_nav_items'] = True
        return context


class DashboardView(views.ListView):
    model = VehiclePhoto
    template_name = 'main/dashboard.html'
    context_object_name = 'vehicle_photos'
