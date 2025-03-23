
from django.urls import path, include

from . import views

urlpatterns = [
    # path('<str:client_id>', views.get_client_by_id),
    # path('', views.client_list),
    path('create', views.add_to_cart),
    path('orderReceived/<str:member_id>', views.get_orders_received_by_member)
]

