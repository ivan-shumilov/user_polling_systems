from rest_framework import permissions
from rest_framework import viewsets, mixins
from ..serializers import PollSerializer, CreateAdminPollSerializer, UpdateAdminPollSerializer, \
    AdminQuestionSerializer, AdminOptionTheQuestionSerializer
from ..models import Poll, Question, OptionTheQuestion


class AdminPollViewSet(viewsets.ReadOnlyModelViewSet, mixins.CreateModelMixin, mixins.UpdateModelMixin,
                       mixins.DestroyModelMixin):
    queryset = Poll.objects
    serializer_class = PollSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_serializer_class(self):
        if self.action in ['create']:
            return CreateAdminPollSerializer
        elif self.action in ['update', 'partial_update']:
            return UpdateAdminPollSerializer
        return PollSerializer

    def get_queryset(self):
        return self.queryset.all()


class AdminQuestionViewSet(viewsets.ReadOnlyModelViewSet, mixins.CreateModelMixin, mixins.UpdateModelMixin,
                           mixins.DestroyModelMixin):
    queryset = Question.objects
    serializer_class = AdminQuestionSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        return self.queryset.all()


class AdminOptionTheQuestionViewSet(viewsets.ReadOnlyModelViewSet, mixins.CreateModelMixin, mixins.UpdateModelMixin,
                                    mixins.DestroyModelMixin):
    queryset = OptionTheQuestion.objects
    serializer_class = AdminOptionTheQuestionSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        return self.queryset.all()
