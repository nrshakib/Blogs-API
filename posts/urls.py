from django.urls import path

from posts import views


urlpatterns = [
    path('posts/', views.PostListCreateApiView.as_view(), name='post-list-create'),
    path('post/<str:identifier>/', views.PostRetrieveUpdateDeleteApiView.as_view(), name='single-post-manage')
]