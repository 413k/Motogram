from django.contrib import admin

from motogram.main.models import Profile, Vehicle, VehiclePhoto


class VehicleInLineAdmin(admin.StackedInline):
    model = Vehicle


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    # inlines = (VehicleInLineAdmin,)
    pass

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    pass

@admin.register(VehiclePhoto)
class VehiclePhotoAdmin(admin.ModelAdmin):
    pass
