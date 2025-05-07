from django.urls import path
from . import views
from authentication.views import mail_user
from authentication.views import verify_code
from authentication.views import update_user_password
from authentication.views import UserListView
from authentication.views import EditUserView
from authentication.auth_component.login import CustomTokenObtainPairView
from authentication.auth_component.logout import LogoutView

 
urlpatterns = [
    # registers a user
    path('user/create/', views.CreateUserView.as_view(), name="create"),

    # List all users
    path("users/", UserListView.as_view(), name="user_list"),

    # Edit one user
    path("users/<int:user_id>/edit/", EditUserView.as_view(), name="edit_user"),

    # login and provide access token
    path('login/', CustomTokenObtainPairView.as_view(), name="get_token"),

    # request access token and log out
    path('logout/', LogoutView.as_view(), name="logout"),

    # request a pin 
    path('mail/', mail_user, name="request_rest_code"),

    # verify pin
    path('verify/', verify_code, name="verify_rest_code"),

    # update password
    path('update_user_password/', update_user_password, name="update_password"),

    # get authentication/permissions will list all while post authentication/permissions/ will create
    path('settings/', views.SettingListCreate.as_view(), name="settings"),


    # update authentication/permissions will list all while post authentication/permissions/ will create
    path('settings/<int:pk>/', views.SettingUpdate.as_view(), name="settings_update"),

    # get/post/delete authentication/permissions/delete/id will delete a individual note
    path('settings/delete/<int:pk>', views.SettingDelete.as_view(), name="settings_delete"),
] 
      