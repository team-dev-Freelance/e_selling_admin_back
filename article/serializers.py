from rest_framework import serializers
from .models import Article


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        # fields = ['label', 'price', 'category', 'member', 'logo']
        exclude = ['active']
