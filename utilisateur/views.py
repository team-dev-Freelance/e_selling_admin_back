from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status as drf_status, status
from utilisateur.serializers import MyTokenObtainPairSerializer


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    def login(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == drf_status.HTTP_200_OK:
            user = self.get_serializer().user
            user.status = True
            user.save()
        return response


class LogoutView(APIView):

    def post(self, request):
        user = request.user
        user.status = False
        user.save()
        return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)

