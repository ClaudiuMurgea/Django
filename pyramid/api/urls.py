from django.urls import path
from . import views

urlpatterns = [
    path('notes/', views.PermissionListCreate.as_view(), name="note-list"),
    path('notes/delete/<int:pk>', views.PermissionDelete.as_view(), name="delete"),
]
