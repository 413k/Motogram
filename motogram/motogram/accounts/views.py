from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.views import generic as views

from motogram.accounts.forms import CreateProfileForm, EditProfileForm
from motogram.accounts.models import Profile
from motogram.common.view_mixins import RedirectToDashboard
from motogram.main.models import Vehicle, VehiclePhoto


class UserRegisterView(RedirectToDashboard, views.CreateView):
    form_class = CreateProfileForm
    template_name = 'accounts/profile_create.html'
    success_url = reverse_lazy('dashboard')


class UserLoginView(auth_views.LoginView):
    template_name = 'accounts/login_page.html'
    success_url = reverse_lazy('dashboard')

    def get_success_url(self):
        if self.success_url:
            return self.success_url
        return super().get_success_url()


class EditProfileView:
    pass


class ChangeUserPasswordView(auth_views.PasswordChangeView):
    template_name = 'accounts/change_password.html'


class ProfileDetailsView(views.DetailView):
    model = Profile
    template_name = 'main/../../templates/accounts/profile_details.html'
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
