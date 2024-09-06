from django.contrib.auth import logout
from rest_framework.views import APIView, Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserInfoSerializer

# Create your views here.


class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'options', 'head']

    def get(self, request):
        user = request.user

        # Serializamos los datos del usuario
        serializer = UserInfoSerializer(user)

        # Añadimos campos adicionales manualmente
        response_data = serializer.data
        response_data.update({
            "sub": user.id,
            "name": f"{user.first_name} {user.last_name}",
            "given_name": user.first_name,
            "family_name": user.last_name,
            "preferred_username": user.username,
        })

        return Response(response_data)



class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ['post', 'options', 'head']

    def options(self, request, *args, **kwargs):
        """Manejo de solicitudes preflight OPTIONS para CORS"""
        response = Response(status=status.HTTP_200_OK)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        return response

    def post(self, request, *args, **kwargs):
        """Cerrar sesión del usuario autenticado"""
        logout(request)
        response = Response(status=status.HTTP_204_NO_CONTENT)
        response["Access-Control-Allow-Origin"] = "*"
        return response
