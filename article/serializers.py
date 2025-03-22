from rest_framework import serializers

from categorie.models import Categorie
from categorie.serializers import CategorieSerializer
from member.serializers import MemberSerializer
from .models import Article


class ArticleSerializer(serializers.ModelSerializer):
    logo = serializers.SerializerMethodField()
    category = CategorieSerializer()
    member = MemberSerializer()
 
    class Meta:
        model = Article
        fields = ['id', 'label', 'price', 'logo',  'description',  'category',  'member']
    def get_logo(self, obj):
            if obj.logo:
                return f"/media/{obj.logo.name}"
            return None

