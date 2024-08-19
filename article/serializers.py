from rest_framework import serializers

from categorie.models import Categorie
from categorie.serializers import CategorieSerializer
from .models import Article


class ArticleSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField(required=False, write_only=True)
    logo = serializers.ImageField(required=False)

    class Meta:
        model = Article
        fields = ['id', 'label', 'price', 'category_id', 'member', 'logo', 'category']



