from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshSlidingView
from api.views import CreateUserView
from api.auth_component.login import CustomTokenObtainPairView
from api.auth_component.logout import LogoutView
from .views import mail_user
from .views import verify_code
from .views import update_user_password
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
    path('mail/', mail_user, name="request_rest_code"),
    path('verify/', verify_code, name="verify_rest_code"),
    path('update_user_password/', update_user_password, name="update_password"),
]