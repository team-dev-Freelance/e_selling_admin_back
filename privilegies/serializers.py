from rest_framework import serializers
from .models import Privilegies


class PrivilegiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Privilegies
        fields = '__all__'
        exclude = ['active']

