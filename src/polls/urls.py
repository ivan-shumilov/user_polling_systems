from rest_framework.routers import DefaultRouter
from .views.admin_views import AdminPollViewSet, AdminQuestionViewSet, AdminOptionTheQuestionViewSet

router = DefaultRouter()
router.register(r'admin-polls', AdminPollViewSet, basename='admin_polls')
router.register(r'admin-questions', AdminQuestionViewSet, basename='admin_questions')
router.register(r'admin-opinions', AdminOptionTheQuestionViewSet, basename='admin_opinions')

urlpatterns = [
    *router.urls,
]
