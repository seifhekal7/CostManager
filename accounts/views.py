from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.permissions import AllowAny 
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer , LoginSerializer

class RegisterView(APIView):
    permission_classes = [AllowAny] 

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # generate tokens
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        return Response({
            "user": {
                "id": user.id,
                "email": user.email,
                "username": user.username,
            },
            "refresh": str(refresh),
            "access": str(access),
        }, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
      
        serializer = LoginSerializer()
        return Response(serializer.data)


    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']

        # نطلع tokens
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        return Response({
            "user": {
                "id": user.id,
                "email": user.email,
                "username": user.username,
            },
            "refresh": str(refresh),
            "access": str(access),
        }, status=status.HTTP_200_OK)
    
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """
        تستقبل refresh token في body:
        {
            "refresh": "<refresh_token_here>"
        }
        """
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response(
                {"detail": "Refresh token is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()   # نحطه في البلاك ليست
        except Exception:
            return Response(
                {"detail": "Invalid refresh token"},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response({"detail": "Logged out successfully"}, status=status.HTTP_205_RESET_CONTENT)