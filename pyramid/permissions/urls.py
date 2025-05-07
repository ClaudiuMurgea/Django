from django.urls import path
from . import views
   
urlpatterns = [
  # get authentication/permissions will list all while post authentication/permissions/ will create
  path('', views.PermissionListCreate.as_view(), name="permission_list"),

  # get/post/delete authentication/permissions/delete/id will delete a individual note
  path('delete/<int:pk>', views.PermissionDelete.as_view(), name="permission_delete"),
]