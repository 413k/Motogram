from django.contrib import admin

from motogram.accounts.models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    # inlines = (VehicleInLineAdmin,)
    pass