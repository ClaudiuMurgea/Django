from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshSlidingView
from api.views import CreateUserView
from api.auth_component.login import CustomTokenObtainPairView
from api.auth_component.logout import LogoutView
from .views import home

# prebuilt views, that allow us to obtain and access our refresh token, bult in to sign in users

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/refresh', TokenRefreshSlidingView.as_view(), name="refresh"),
    path('api-auth/', include("rest_framework.urls")),
    path('api/', include('api.urls')),
    path("welcome/", home, name="home"),
]