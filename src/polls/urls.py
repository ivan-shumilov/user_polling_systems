from rest_framework.routers import DefaultRouter
from .views.admin_views import AdminPollViewSet

router = DefaultRouter()
router.register(r'admin-polls', AdminPollViewSet, basename='admin_polls')

urlpatterns = [
    *router.urls,
]
