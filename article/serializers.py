from rest_framework import serializers

from categorie.models import Categorie
from categorie.serializers import CategorieSerializer
from .models import Article


class ArticleSerializer(serializers.ModelSerializer):
    category = CategorieSerializer(read_only=True)
    category_id = serializers.IntegerField(required=False, write_only=True)
    logo = serializers.ImageField(required=True)

    class Meta:
        model = Article
        fields = ['id', 'label', 'price', 'category_id', 'member', 'logo', 'category']

    # def get_logo_url(self, obj):
    #     if obj.logo:
    #         request = self.context.get('request')
    #         return request.build_absolute_uri(obj.logo.url) if request else obj.logo.url
    #     return None

