from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Post, User
from .permissions import IsAuthorOrReadOnlyPermission
from .serializers import PostSerializer, UserSerializer
from .filters import PostFilter


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend]
    filter_class = PostFilter
    permission_classes = [IsAuthorOrReadOnlyPermission]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnlyPermission]


class UserList(APIView):
    def get(self, request, username):
        users = User.objects.filter(username=username)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

# class UserList(generics.ListAPIView):
#     serializer_class = UserSerializer
#     queryset = User.objects.all()
#
#     def get_queryset(self):
#         username = self.request.query_params.get('username', None)
#         if username is None:
#             return self.queryset
#
#         queryset = self.queryset.filter(username=username)
#         return queryset
