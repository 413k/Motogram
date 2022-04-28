from django.urls import path

from motogram.main.views.generic import HomeView, DashboardView
from motogram.main.views.vehicle_photos import VehiclePhotoDetailsView, EditVehiclePhotoView, \
    like_vehicle_photo, CreateVehiclePhotoView
from motogram.main.views.vehicles import CreateVehicleView, EditVehicleView, DeleteVehicleView

urlpatterns = [
    # Main things
    path('', HomeView.as_view(), name='index'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),

    # Photo
    path('photo/details/<int:pk>/', VehiclePhotoDetailsView.as_view(), name='vehicle photo details'),
    path('photo/add/', CreateVehiclePhotoView.as_view(), name='create vehicle photo'),
    path('photo/edit/<int:pk>/', EditVehiclePhotoView.as_view(), name='edit vehicle photo'),
    path('photo/like/<int:pk>', like_vehicle_photo, name='like vehicle photo'),

    # Vehicle
    path('vehicle/add/', CreateVehicleView.as_view(), name='create vehicle'),
    path('vehicle/edit/<int:pk>/', EditVehicleView.as_view(), name='edit vehicle'),
    path('vehicle/delete/<int:pk>/', DeleteVehicleView.as_view(), name='delete vehicle'),

]
