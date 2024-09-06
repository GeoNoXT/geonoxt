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
    http_method_names = ['get', 'options']

    def get(self, request, *args, **kwargs):
        # Hacer logout
        logout(request)

        # Obtener la URL de retorno desde los parámetros
        next_url = request.GET.get('next', None)

        if next_url:
            # Redirigir a la URL de retorno si está presente
            return HttpResponseRedirect(next_url)
        else:
            # Devolver una respuesta JSON indicando éxito si no hay URL de retorno
            return Response({'detail': 'Logout successful'}, status=status.HTTP_204_NO_CONTENT)
