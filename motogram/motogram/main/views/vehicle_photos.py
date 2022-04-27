from django.contrib.auth import mixins as auth_mixin
from django.urls import reverse_lazy
from django.views import generic as views
from django.shortcuts import render, redirect

from motogram.main.models import VehiclePhoto


class VehiclePhotoDetailsView(auth_mixin.LoginRequiredMixin, views.DetailView):
    model = VehiclePhoto
    template_name = 'main/photo_details.html'
    context_object_name = 'vehicle_photo'

    def get_queryset(self):
        return super().get_queryset().prefetch_related('tagged_vehicles')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_owner'] = self.object.user == self.request.user
        return context


class CreateVehiclePhotoView(auth_mixin.LoginRequiredMixin, views.CreateView):
    model = VehiclePhoto
    template_name = 'main/photo_create.html'
    fields = ('photo', 'description', 'tagged_vehicles')
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


def like_vehicle_photo(request, pk):
    vehicle_photo = VehiclePhoto.objects.get(pk=pk)
    vehicle_photo.likes += 1
    vehicle_photo.save()
    return redirect('vehicle photo details', pk)


def edit_vehicle_photo(request):
    return render(request, 'main/photo_edit.html')
