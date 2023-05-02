from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from ads.models import Selection
from ads.permissions import IsOwner
from ads.serializers import SelectionSerializer, SelectionListSerializer, SelectionCreateSerializer, \
    SelectionDetailSerializer


class SelectionViewSet(ModelViewSet):
    queryset = Selection.objects.order_by('name')
    default_serializer_class = SelectionSerializer

    default_permission = [AllowAny]
    permission = {
        'create': [IsAuthenticated],
        'update': [IsAuthenticated, IsOwner],
        'partial_update': [IsAuthenticated, IsOwner],
        'destroy': [IsAuthenticated, IsOwner],
    }

    serializers = {
        "list": SelectionListSerializer,
        'create': SelectionCreateSerializer,
        'retrieve': SelectionDetailSerializer,
    }

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.default_serializer_class)

    def get_permissions(self):
        return [permission() for permission in self.permission.get(self.action, self.default_permission)]
