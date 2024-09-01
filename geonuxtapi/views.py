from django.shortcuts import render
from rest_framework.views import APIView, Response
from rest_framework.permissions import IsAuthenticated
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
            "sub": str(user.id),
            "name": f"{user.first_name} {user.last_name}",
        })

        return Response(response_data)
