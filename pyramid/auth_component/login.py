from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import login


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer  # Use default JWT serializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)  # Generate token

        # Log in the authenticated user
        username = request.data.get("username")
        user = self.get_user(username)
        if user:
            login(request, user)

        return response

    def get_user(self, username):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        return User.objects.filter(username=username).first()
