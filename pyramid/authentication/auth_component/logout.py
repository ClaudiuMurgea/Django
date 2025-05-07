from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import logout

# When logging out, the jwt package was modified to blacklist the access token of the user
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    #Blacklist Token
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()  # Blacklist the refresh token

            # logout(request)  # Logout the user session

            return Response({"message": "Successfully logged out" + refresh_token}, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=400)
