from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import MyUser
from .serializers import RegisterSerializer


class RegisterView(APIView):
    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response("You have successfully registered.", status=status.HTTP_201_CREATED)


class ActivationView(APIView):
    def get(self, request, activation_code):
        user = MyUser.objects.get(activation_code=activation_code)
        if not user:
            return Response('Sorry, user was not found.', status=status.HTTP_400_BAD_REQUEST)
        user.activation_code = ''
        user.is_active = True
        user.save()
        return Response('User was successfully activated.', status=status.HTTP_200_OK)
