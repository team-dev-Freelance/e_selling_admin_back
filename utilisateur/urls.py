
from django.urls import path, include

from . import views

urlpatterns = [
    path('<str:user_id>', views.get_user_by_id),
    # path('', views.categorie_list),
    # path('create', views.categorie_create),
    # path('update/<str:pk>', views.categorie_update),
    path('createadmin', views.create_admin_user),
    path('list', views.user_list),
]

