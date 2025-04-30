from django.urls import path
from . import views
from api.views import mail_user
from api.views import verify_code
from api.views import update_user_password
from api.auth_component.login import CustomTokenObtainPairView
from api.auth_component.logout import LogoutView


urlpatterns = [
    # registers a user
    path('user/register/', views.CreateUserView.as_view(), name="register"),

    # login and provide access token
    path('token/', CustomTokenObtainPairView.as_view(), name="get_token"),

    # request access token and log out
    path('logout/', LogoutView.as_view(), name="logout"),

    # request a pin 
    path('mail/', mail_user, name="request_rest_code"),

    # verify pin
    path('verify/', verify_code, name="verify_rest_code"),

    # update password
    path('update_user_password/', update_user_password, name="update_password"),

    # get api/notes will list all while post api/notes/ will create
    path('notes/', views.PermissionListCreate.as_view(), name="note-list"),

    # get/post/delete api/notes/delete/id will delete a individual note
    path('notes/delete/<int:pk>', views.PermissionDelete.as_view(), name="delete"),
] 
      