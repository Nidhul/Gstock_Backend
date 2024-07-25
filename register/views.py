# views.py

from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .forms import UserRegistrationForm
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes


class RegisterView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        form = UserRegistrationForm(request.data)
        if form.is_valid():
            user = form.save()
            response_data = {"user_registered_successfully"}
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = TokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        user = User.objects.get(username=request.data['username'])
        response.data['admin'] = user.is_staff
        return response
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_non_admin_users(request):
    if request.user.is_staff:
        non_admin_users = User.objects.filter(is_staff=False)
        user_data = [{"username": user.username, "password": user.password,"id":user.id} for user in non_admin_users]
        return Response(user_data, status=status.HTTP_200_OK)
    return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user(request, user_id):
    if request.user.is_staff:
        try:
            user = User.objects.get(id=user_id, is_staff=False)
            user.delete()
            return Response({"User deleted successfully."}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"detail": "User not found or you do not have permission to delete this user."}, status=status.HTTP_404_NOT_FOUND)
    return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)
