from rest_framework import serializers

from categorie.models import Categorie
from categorie.serializers import CategorieSerializer
from .models import Article


class ArticleSerializer(serializers.ModelSerializer):
    category = CategorieSerializer(read_only=True)  # Pour les requêtes GET
    category_id = serializers.PrimaryKeyRelatedField(queryset=Categorie.objects.all(),
                                                         write_only=True)

    class Meta:
        model = Article
        fields = ['label', 'price', 'category', 'category_id', 'member', 'logo']
        # exclude = ['active']
