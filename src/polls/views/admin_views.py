from rest_framework import permissions
from rest_framework import viewsets, mixins
from ..serializers import AdminPollSerializer, CreateAdminPollSerializer, UpdateAdminPollSerializer
from ..models import Poll


class AdminPollViewSet(viewsets.ReadOnlyModelViewSet, mixins.CreateModelMixin, mixins.UpdateModelMixin,
                       mixins.DestroyModelMixin):
    queryset = Poll.objects
    serializer_class = AdminPollSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_serializer_class(self):
        if self.action in ['create']:
            return CreateAdminPollSerializer
        elif self.action in ['update', 'partial_update']:
            return UpdateAdminPollSerializer
        return AdminPollSerializer

    def get_queryset(self):
        return self.queryset.all()
