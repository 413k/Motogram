from django.urls import path, reverse_lazy
from django.views.generic import RedirectView

from motogram.accounts.views import UserLoginView, UserRegisterView, ProfileDetailsView, ChangeUserPasswordView

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login user'),

    # Profile
    path('<int:pk>/', ProfileDetailsView.as_view(), name='profile details'),
    path('register/', UserRegisterView.as_view(), name='register'),
    # path('profile/edit/', , name='edit profile'),
    # path('profile/delete/', delete_profile, name='delete profile'),

    path('edit-password/', ChangeUserPasswordView.as_view(), name='change password'),
    path('password_change_done/', RedirectView.as_view(url=reverse_lazy('dashboard')), name='password_change_done'),

]
