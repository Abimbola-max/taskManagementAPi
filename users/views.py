from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({"message": "Registration successful"}, status=status.HTTP_201_CREATED)

login_request_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['email', 'password'],
    properties={
        'email': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL),
        'password': openapi.Schema(type=openapi.TYPE_STRING, format='password'),
    },
)

@swagger_auto_schema(method='post', request_body=login_request_body)
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_view(request):
    email = request.data.get('email')
    password = request.data.get('password')
    if not email or not password:
        return Response({"detail": "Email and password required."}, status=400)
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({"detail": "Invalid credentials."}, status=401)
    user = authenticate(username=user.username, password=password)
    if not user:
        return Response({"detail": "Invalid credentials."}, status=401)
    refresh = RefreshToken.for_user(user)
    return Response({
        "refresh": str(refresh),
        "access": str(refresh.access_token)
    })
