from django.shortcuts import render, redirect
from django.contrib.auth import mixins as auth_mixin

from django.views import generic as views
from motogram.main.forms import CreateProfileForm, EditProfileForm, DeleteProfileForm
from motogram.main.models import Vehicle, VehiclePhoto, Profile
from motogram.main.views.helpers import get_profile


class ProfileDetailsView(views.DetailView):
    model = Profile
    template_name = 'main/profile_details.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # self.object is a Profile instance
        vehicles = list(Vehicle.objects.filter(user_id=self.object.user_id))

        vehicle_photos = VehiclePhoto.objects \
            .filter(tagged_vehicles__in=vehicles) \
            .distinct()

        total_likes_count = sum(pp.likes for pp in vehicle_photos)
        total_vehicle_photos_count = len(vehicle_photos)

        context.update({
            'total_likes_count': total_likes_count,
            'total_vehicle_photos_count': total_vehicle_photos_count,
            'is_owner': self.object.user_id == self.request.user.id,
            'vehicles': vehicles,
        })

        return context


def crud_action(request, form_class, success_url, instance, template_name):
    if request.method == 'POST':
        form = form_class(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect(success_url)
    else:
        form = form_class(instance=instance)

    context = {
        'form': form,
    }

    return render(request, template_name, context)


def create_profile(request):
    return crud_action(request, CreateProfileForm, 'index', Profile(), 'main/profile_create.html')


def edit_profile(request):
    return crud_action(request, EditProfileForm, 'profile details', get_profile(), 'main/profile_edit.html')


def delete_profile(request):
    return crud_action(request, DeleteProfileForm, 'index', get_profile(), 'main/profile_delete.html')

# def create_profile(request):
#     if request.method == 'POST':
#         form = CreateProfileForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('index')
#     else:
#         form = CreateProfileForm()
#
#     context = {
#         'form': form,
#     }
#
#     return render(request, 'profile_create.html', context)
#
#
# def edit_profile(request):
#     profile = get_profile()
#
#     if request.method == 'POST':
#         form = EditProfileForm(request.POST, instance=profile)
#         if form.is_valid():
#             form.save()
#             return redirect('profile details')
#     else:
#         form = EditProfileForm(instance=profile)
#
#     context = {
#         'form': form,
#     }
#     return render(request, 'profile_edit.html', context)
#
# def delete_profile(request):
#     return render(request, 'profile_delete.html')
