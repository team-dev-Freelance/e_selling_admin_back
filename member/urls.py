
from django.urls import path, include

from . import views

urlpatterns = [
    path('<str:member_id>', views.get_member_by_id),
    path('', views.member_list),
    path('create', views.create_member),
    path('deleteAll', views.delete_all_members),
    # path('update/<str:pk>', views.categorie_update),
    # path('delete/<str:pk>', views.categorie_delete),
]

