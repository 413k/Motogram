from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator
from django.db import models

from motogram.main.validators import validate_only_letters, validate_file_max_size_in_mb

UserModel = get_user_model()


class Profile(models.Model):
    FIRST_NAME_MAX_LENGTH = 30
    FIRST_NAME_MIN_LENGTH = 2

    LAST_NAME_MAX_LENGTH = 30
    LAST_NAME_MIN_LENGTH = 2

    MALE = 'Male'
    FEMALE = 'Female'
    DO_NOT_SHOW = 'Do not show'

    GENDERS = [(x, x) for x in (MALE, FEMALE, DO_NOT_SHOW)]

    first_name = models.CharField(
        max_length=FIRST_NAME_MAX_LENGTH,
        validators=(
            MinLengthValidator(FIRST_NAME_MIN_LENGTH),
            validate_only_letters,

        )

    )

    last_name = models.CharField(
        max_length=LAST_NAME_MAX_LENGTH,
        validators=(
            MinLengthValidator(LAST_NAME_MIN_LENGTH),
            validate_only_letters,

        )

    )

    picture = models.URLField()

    date_of_birth = models.DateField(
        null=True,
        blank=True,

    )

    description = models.TextField(
        null=True,
        blank=True,

    )

    email = models.EmailField(
        null=True,
        blank=True,

    )

    gender = models.CharField(
        max_length=max(len(x) for x, _ in GENDERS),
        choices=GENDERS,
        null=True,
        blank=True,
        default=DO_NOT_SHOW,
    )

    user = models.OneToOneField(
        UserModel,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


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
    photo = models.ImageField(
        validators=(
            validate_file_max_size_in_mb,
        )
    )

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
