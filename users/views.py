from django.db.models import Count, Q
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet

from ads.models import User

from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView

from users.models import Location
from users.serializers import UserSerializer, UserCreateSerializer, UserUpdateSerializer, UserListSerializer, \
    LocationSerializer


class UserPagination(PageNumberPagination):
    page_size = 4


class UserListView(ListAPIView):
    queryset = User.objects.annotate(total_ads=Count('ad', filter=Q(ad__is_published=True))).order_by('username')
    serializer_class = UserListSerializer
    pagination_class = UserPagination


class UserDetailView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer


class UserUpdateView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer


class UserDeleteView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class LocationViewSet(ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
