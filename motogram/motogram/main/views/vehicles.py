from django.urls import reverse_lazy
from django.views import generic as views

from motogram.main.forms import CreateVehicleForm, EditVehicleForm, DeleteVehicleForm


class CreateVehicleView(views.CreateView):
    template_name = 'main/vehicle_create.html'
    form_class = CreateVehicleForm
    success_url = reverse_lazy('dashboard')


    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class EditVehicleView(views.UpdateView):
    template_name = 'main/vehicle_edit.html'
    form_class = EditVehicleForm


class DeleteVehicleView(views.DeleteView):
    template_name = 'main/vehicle_delete.html'
    form_class = DeleteVehicleForm
