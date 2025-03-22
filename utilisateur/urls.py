
from django.urls import path, include

from . import views

urlpatterns = [
    # path('<str:pk>', views.categorie_detail),
    # path('', views.categorie_list),
    # path('create', views.categorie_create),
    # path('update/<str:pk>', views.categorie_update),
    path('createadmin', views.create_admin_user),
    path('list', views.user_list),
]

