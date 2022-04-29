import logging
from datetime import date

from django import test as django_test
from django.contrib.auth import get_user_model
from django.urls import reverse

from motogram.accounts.models import Profile
from motogram.main.models import Vehicle, VehiclePhoto

UserModel = get_user_model()


class ProfileDetailsView(django_test.TestCase):
    VALID_USER_CREDENTIALS = {
        'username': 'testuser',
        'password': '12345qew',
    }
    VALID_PROFILE_DATA = {
        'first_name': 'Test',
        'last_name': 'User',
        'picture': 'https://test.picture/url.png',
        'date_of_birth': date(1900, 4, 13),
    }

    VALID_VEHICLE_DATA = {
        'brand': 'BMW',
        'vehicle_type': Vehicle.CAR,
    }

    VALID_VEHICLE_PHOTO_DATA = {
        'photo': 'asd.jpg',
        'publication_date': date.today(),
    }

    def __create_user(self, **credentials):
        return UserModel.objects.create_user(**credentials)

    def __create_valid_user_and_profile(self):
        user = self.__create_user(**self.VALID_USER_CREDENTIALS)
        profile = Profile.objects.create(
            **self.VALID_PROFILE_DATA,
            user=user,
        )
        return (user, profile)

    def __create_vehicle_and_vehicle_photo_for_user(self, user):
        vehicle = Vehicle.objects.create(
            **self.VALID_VEHICLE_DATA,
            user=user,
        )
        vehicle_photo = VehiclePhoto.objects.create(
            **self.VALID_VEHICLE_PHOTO_DATA,
            user=user,

        )
        vehicle_photo.tagged_vehicles.add(vehicle)
        vehicle_photo.save()
        return (vehicle, vehicle_photo)

    def __get_response_for_profile(self, profile):
        return self.client.get(reverse('profile details', kwargs={'pk': profile.pk}))

    def test_when_opening_not_existing_profile__expect_404(self):
        response = self.client.get(reverse('profile details', kwargs={
            'pk': 1,
        }))
        self.assertEqual(404, response.status_code)

    def test_expect_correct_template(self):
        _, profile = self.__create_valid_user_and_profile()
        self.__get_response_for_profile(profile)
        self.assertTemplateUsed('accounts/profile_details.html')

    def test_when_user_is_owner__expect_this_owner_to_be_true(self):
        _, profile = self.__create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)

        response = self.__get_response_for_profile(profile)

        self.assertTrue(response.context['is_owner'])

    def test_when_user_is_not_owner__expect_this_owner_to_be_false(self):
        _, profile = self.__create_valid_user_and_profile()
        credentials = {
            'username': 'testuser2',
            'password': '12345qwe',

        }

        self.__create_user(**credentials)

        self.client.login(**credentials)

        response = self.__get_response_for_profile(profile)

        self.assertFalse(response.context['is_owner'])

    def test_when_no_photo_likes__expect_total_likes_count_to_be_0(self):
        user, profile = self.__create_valid_user_and_profile()
        self.__create_vehicle_and_vehicle_photo_for_user(user)
        response = self.__get_response_for_profile(profile)

        self.assertEqual(0, response.context['total_likes_count'])

    def test_when_photo_likes__expect_total_likes_count_to_be_correct(self):
        likes = 3
        user, profile = self.__create_valid_user_and_profile()
        _, vehicle_photo = self.__create_vehicle_and_vehicle_photo_for_user(user)
        vehicle_photo.likes = likes
        vehicle_photo.save()

        response = self.__get_response_for_profile(profile)

        self.assertEqual(likes, response.context['total_likes_count'])

    def test_when_no_photos__no_photos_count(self):
        # TODO same as likes
        pass

    def test_when_user_has_vehicles__expect_to_return_only_users_vehicles(self):
        user, profile = self.__create_valid_user_and_profile()
        credentials = {
            'username': 'testuser2',
            'password': '12345qwe',
        }
        user2 = self.__create_user(**credentials)
        # Create a vehicle/s for a different user
        vehicle, _ = self.__create_vehicle_and_vehicle_photo_for_user(user)

        self.__create_vehicle_and_vehicle_photo_for_user(user2)

        response = self.__get_response_for_profile(profile)

        self.assertListEqual(
            [vehicle],
            response.context['vehicles'],
        )

    def test_when_user_has_no_vehicles__vehicles_should_be_empty(self):
        _, profile = self.__create_valid_user_and_profile()

        response = self.__get_response_for_profile(profile)
        self.assertListEqual(
            [],
            response.context['vehicles'],
        )

    def test_when_no_vehicles__likes_and_photos_should_be_0(self):
        pass
