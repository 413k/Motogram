from django.urls import path

from motogram.accounts.views import UserLoginView

urlpatterns = (
    path('login/', UserLoginView.as_view(), name='login user'),
    # path(),
    # path(),
    # path(),
    # path(),
)
