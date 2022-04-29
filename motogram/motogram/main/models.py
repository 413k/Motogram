from cloudinary import models as cloudinary_models
from django.contrib.auth import get_user_model
from django.db import models

from motogram.common.validators import MaxFileSizeInMbValidator

UserModel = get_user_model()


class Vehicle(models.Model):
    VEHICLE_MAX_LENGTH = 30

    CAR = 'Car'
    MOTOR_CYCLE = 'Motorycle'
    AIRPLANE = 'Airplane'
    HELICOPTER = 'Helicopter'
    BICYCLE = 'Bicycle'

    TYPES = [(x, x) for x in (CAR, MOTOR_CYCLE, AIRPLANE, HELICOPTER, BICYCLE)]

    # MIN_DATE = datetime.date(1800, 1, 1)

    brand = models.CharField(
        max_length=VEHICLE_MAX_LENGTH,

    )

    vehicle_type = models.CharField(
        max_length=max(len(x) for (x, _) in TYPES),
        choices=TYPES,

    )

    year_of_creation = models.DateField(
        null=True,
        blank=True,
        # validators=(
        #     MinDateValidator(),
        # )

    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.brand}-{self.vehicle_type}'


class VehiclePhoto(models.Model):

    photo = cloudinary_models.CloudinaryField('image')

    description = models.TextField(
        null=True,
        blank=True,
    )

    publication_date = models.DateTimeField(
        auto_now_add=True,

    )

    likes = models.IntegerField(
        default=0,
    )

    tagged_vehicles = models.ManyToManyField(
        Vehicle,
        # Validate at least one vehicle
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        if self.description:
            return f'{self.description}'
        else:
            return f'Photo with {self.likes} likes'
