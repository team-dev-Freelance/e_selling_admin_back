from rest_framework_simplejwt.views import TokenObtainPairView

from utilisateur.serializers import MyTokenObtainPairSerializer


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
