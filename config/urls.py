
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('accounts.urls')),
    path('api/', include('posts.urls')),
]
