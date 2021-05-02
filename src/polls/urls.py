from rest_framework.routers import DefaultRouter
from django.urls import path
from .views.admin_views import AdminPollViewSet, AdminQuestionViewSet, AdminOptionTheQuestionViewSet
from .views.client_views import PollsAPIView

router = DefaultRouter()
router.register(r'admin-polls', AdminPollViewSet, basename='admin_polls')
router.register(r'admin-questions', AdminQuestionViewSet, basename='admin_questions')
router.register(r'admin-opinions', AdminOptionTheQuestionViewSet, basename='admin_opinions')

urlpatterns = [
    *router.urls,
    path('polls/', PollsAPIView.as_view(), name="polls"),
]
