from django.urls import path

from motogram.main.views.generic import HomeView, DashboardView
from motogram.main.views.profiles import ProfileDetailsView, create_profile, edit_profile, delete_profile
from motogram.main.views.vehicle_photos import VehiclePhotoDetailsView, edit_vehicle_photo, \
    like_vehicle_photo, CreateVehiclePhotoView
from motogram.main.views.vehicles import CreateVehicleView, EditVehicleView, DeleteVehicleView

urlpatterns = [
    # Main things
    path('', HomeView.as_view(), name='index'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),

    # Profile
    path('profile/<int:pk>/', ProfileDetailsView.as_view(), name='profile details'),
    path('profile/create/', create_profile, name='create profile'),
    path('profile/edit/', edit_profile, name='edit profile'),
    path('profile/delete/', delete_profile, name='delete profile'),

    # Photo
    path('photo/details/<int:pk>/', VehiclePhotoDetailsView.as_view(), name='vehicle photo details'),
    path('photo/add/', CreateVehiclePhotoView.as_view(), name='create vehicle photo'),
    path('photo/edit/<int:pk>/', edit_vehicle_photo, name='edit vehicle photo'),
    path('photo/like/<int:pk>', like_vehicle_photo, name='like vehicle photo'),

    # Vehicle
    path('vehicle/add/', CreateVehicleView.as_view(), name='create vehicle'),
    path('vehicle/edit/<int:pk>/', EditVehicleView.as_view(), name='edit vehicle'),
    path('vehicle/delete/<int:pk>/', DeleteVehicleView.as_view(), name='delete vehicle'),

]
