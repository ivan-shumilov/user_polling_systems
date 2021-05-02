from rest_framework import views
from datetime import date
from rest_framework import permissions
from rest_framework.response import Response
from ..models import Poll
from ..serializers import PollSerializer


class PollsAPIView(views.APIView):
    permission_classes = []

    def get(self, request):
        today = date.today()
        return Response(PollSerializer(Poll.objects.filter(date_start__lte=today, date_finish__gt=today),
                                       many=True).data)
