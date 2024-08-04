from rest_framework import serializers

from privilegies.serializers import PrivilegiesSerializer
from .models import Role


class RoleSerializer(serializers.ModelSerializer):
    privileges = PrivilegiesSerializer(many=True, read_only=True)

    class Meta:
        model = Role
        exclude = ['active']

    def get_privileges(self, obj):
        return obj.get_privileges(obj.role)

    def create(self, validated_data):
        privileges_data = validated_data.pop('privileges', None)
        role_instance = Role.objects.create(**validated_data)
        if privileges_data:
            role_instance.privileges.set(privileges_data)
        else:
            role_instance.privileges.set(role_instance.get_privileges(role_instance.role))
        return role_instance
