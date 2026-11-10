from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from accounts import views


urlpatterns = [
    path('register/', views.UserRegistrationView.as_view(), name='user-create'),
    path('login/', views.CustomLoginView.as_view(), name='login-view'),

    path('token-refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('logout/', views.LogoutView.as_view(), name='logout-view'),

    path('change-password/', views.ChangePasswordView.as_view(), name='change-password')
]