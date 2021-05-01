from rest_framework.viewsets import GenericViewSet
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from .models import User
from .serializers import SignInSerializer, UserSerializer


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return None


class LoginUserView(GenericViewSet):
    """
        User authorization. If the user is not logged in or does not have a token, the system will show - errors: true
        else it will errors=false and token.
    """
    queryset = User.objects
    serializer_class = SignInSerializer
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.get_authenticated_user(request)
        try:
            token = Token.objects.get(user=user)
            return Response({'user': UserSerializer(token.user, many=False).data, 'token': token.key,
                             'errors': False})
        except Token.DoesNotExist:
            return Response({'errors': True}, status=status.HTTP_400_BAD_REQUEST)
