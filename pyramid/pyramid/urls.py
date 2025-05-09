from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from .views import home

# prebuilt views, that allow us to obtain and access our refresh token, bult in to sign in users

urlpatterns = [
    path('admin/', admin.site.urls),
    path('authentication/token/refresh', TokenRefreshView.as_view(), name="refresh"),
    path('api-auth/', include("rest_framework.urls")),
    path('authentication/', include('authentication.urls')),
    path("welcome/", home, name="home"),
]