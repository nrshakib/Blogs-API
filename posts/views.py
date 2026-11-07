from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from posts.models import PostModel
from posts.serializers import PostSerializer

class PostListCreateApiView(GenericAPIView, ListModelMixin, CreateModelMixin):
    queryset = PostModel.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        data = self.list(request, *args, **kwargs)

        return Response({
            'message': 'Data retrieved successfully',
            'data': data.data
        }, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = self.create(request, *args, **kwargs)

        return Response({
                'message': 'Post created successfully',
                'data': data.data
            }, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save(author= self.request.user)

class PostRetrieveUpdateDeleteApiView(GenericAPIView, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):
    queryset = PostModel.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        identifier = self.kwargs.get('identifier')

        if identifier.isdigit():
            return get_object_or_404(self.get_queryset(),id=int(identifier))
        else:
            return get_object_or_404(self.get_queryset(),slug=identifier)
        
    def get(self, request, *args, **kwargs):
        data= self.retrieve(request, *args, **kwargs)

        return Response({
            'message': 'Post retrieved successfully',
            'data': data.data
        }, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        data = self.update(request, *args, **kwargs)

        return Response({
                'message': 'Post updated successfully',
                'data': data.data
            }, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        data= self.partial_update(request, *args, **kwargs)

        return Response({
                'message': 'Post updated successfully',
                'data': data.data
            }, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        data = self.destroy(request, *args, **kwargs)

        return Response({
                'message': 'Post deleted successfully',
                'data': None
            }, status=status.HTTP_200_OK)