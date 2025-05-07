from django.shortcuts import render
from .serializers import PermissionSerializer
from .models import Permission
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

# Create your views here.

class PermissionListCreate(generics.ListCreateAPIView):
    serializer_class = PermissionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Permission.objects.filter(author=user)

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(author=self.request.user)
        else:
            print(serializer.errors)


class PermissionDelete(generics.DestroyAPIView):
    serializer_class = PermissionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Permission.objects.filter(author=user)