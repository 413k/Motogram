from django.contrib import admin

from motogram.main.models import Vehicle, VehiclePhoto


class VehicleInLineAdmin(admin.StackedInline):
    model = Vehicle


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    pass


@admin.register(VehiclePhoto)
class VehiclePhotoAdmin(admin.ModelAdmin):
    pass
