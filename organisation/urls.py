# urls.py dans l'application `organisation`

from django.urls import path
from .views import OrganisationViewSet

urlpatterns = [
    path('organisations/<int:organisation_id>/members/', OrganisationViewSet.list_members, name='list_members'),
]
