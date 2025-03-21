
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.role_list),
    path('create', views.role_create),
    path('update/<str:pk>', views.role_update),
    path('delete/<str:pk>', views.role_delete),
]

