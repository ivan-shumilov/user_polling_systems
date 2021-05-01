from rest_framework.routers import DefaultRouter
from .views import LoginUserView

router = DefaultRouter()
router.register(r'login', LoginUserView, basename='sign_in')

urlpatterns = [
    *router.urls,
]
