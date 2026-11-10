from django.urls import path

from accounts import views


urlpatterns = [
    path('register/', views.UserRegistrationView.as_view(), name='user-create'),
    path('login/', views.CustomLoginView.as_view(), name='login-view')
]