from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshSlidingView
from api.views import CreateUserView
from auth.login import CustomTokenObtainPairView
from auth.logout import LogoutView
from .views import simple_mail
# prebuilt views, that allow us to obtain and access our refresh token, bult in to sign in users


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/register/', CreateUserView.as_view(), name="register"),
    path('api/token/', CustomTokenObtainPairView.as_view(), name="get_token"),
    path('api/token/refresh', TokenRefreshSlidingView.as_view(), name="refresh"),
    path('api-auth/', include("rest_framework.urls")),
    path('api/logout/', LogoutView.as_view(), name="logout"),
    path('api/', include('api.urls')),
    path("test/", include("myapp.urls")),
    path('mail', simple_mail)
]
