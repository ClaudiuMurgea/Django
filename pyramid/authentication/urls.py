from django.urls import path
from . import views
from authentication.auth_component.login import CustomTokenObtainPairView
from authentication.auth_component.logout import LogoutView

 
urlpatterns = [
    # registers a user
    path('user/create/', views.RegisterUserAPIView.as_view(), name="create"),

    # List all users
    path("users/", views.UserListView.as_view(), name="user_list"),

    # Edit one user
    path("users/<int:pk>/edit/", views.UpdateUserAPIView.as_view(), name="edit_user"),

    # login and provide access token
    path('login/', CustomTokenObtainPairView.as_view(), name="get_token"),

    # request access token and log out
    path('logout/', LogoutView.as_view(), name="logout"),

    # request a pin 
    path('mail/', views.mail_user, name="request_rest_code"),

    # verify pin
    path('verify/', views.verify_code, name="verify_rest_code"),

    # update password
    path('update_user_password/', views.update_user_password, name="update_password"),

    # unlock user by id
    path('unlock-user/<int:pk>/', views.UnlockUserAPIView.as_view(), name="unlock_user"),

    # serve groups and settings
    path('role/settings/', views.RoleSettingsAPIView.as_view(), name="role_settings"),

    # get authentication/permissions will list all while post authentication/permissions/ will create
    path('settings/', views.SettingsListCreate.as_view(), name="settings"),

    # update authentication/permissions will list all while post authentication/permissions/ will create
    path('settings/<int:pk>/', views.SettingsUpdate.as_view(), name="settings_update"),

    # get/post/delete authentication/permissions/delete/id will delete a individual note
    path('settings/delete/<int:pk>', views.SettingsDelete.as_view(), name="settings_delete"),

    # asign the given group to the user with the given username
    path('assign-role/', views.AssignUserToGroupAPIView.as_view(), name='assign_role'),
] 
      