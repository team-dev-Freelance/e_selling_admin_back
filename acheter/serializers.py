from rest_framework import serializers
from .models import Acheter


class AcheterSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Acheter
        fields = ['client', 'article', 'quantity', 'createDate', 'active', 'total_price']

    def get_total_price(self, obj):
        return obj.get_total_price()