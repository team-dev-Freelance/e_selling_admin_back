# views.py

from rest_framework import viewsets
from .models import Cart
from .serializers import CartWithItemsSerializer


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartWithItemsSerializer

    def get_serializer_context(self):
        # Inclut l'objet `request` dans le contexte du sérialiseur
        return {'request': self.request}
