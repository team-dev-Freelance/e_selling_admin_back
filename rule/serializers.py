from rest_framework import serializers

from privilegies.serializers import PrivilegiesSerializer
from .models import Role


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'role']

    
