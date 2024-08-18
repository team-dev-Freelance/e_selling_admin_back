from rest_framework import serializers

# from .models import Member
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from organisation.models import Organisation
from organisation.serializers import OrganisationSerializer
from rule.models import Role
from rule.serializers import RoleSerializer
from utilisateur.models import Member


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Ajouter des données personnalisées au token si nécessaire
        return token


class MemberSerializer(serializers.ModelSerializer):
    organisation = OrganisationSerializer(read_only=True)
    organisation_id = serializers.PrimaryKeyRelatedField(queryset=Organisation.objects.all(), write_only=True)
    rule = RoleSerializer(read_only=True)
    rule_id = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all(), write_only=True)

    class Meta:
        model = Member
        fields = ['email', 'username', 'phone', 'organisation', 'organisation_id', 'rule', 'rule_id']

    def validate_phone(self, value):
        if not value.startswith(('62', '65', '67', '68', '69')):
            raise serializers.ValidationError('Le numéro doit commencer par 62, 65, 67, 68 ou 69.')
        if len(value) != 9 or not value.isdigit():
            raise serializers.ValidationError('Le numéro de téléphone doit avoir 9 chiffres.')
        return value

    def create(self, validated_data):
        rule_id = validated_data.pop('rule_id')
        role = Role.objects.get(id=rule_id)
        organisation_id = validated_data.pop('organisation_id', None)
        if organisation_id:
            organisation = Organisation.objects.get(id=organisation_id)
            member = Member.objects.create(rule=role, organisation=organisation, **validated_data)
        else:
            member = Member.objects.create(rule=role, **validated_data)
        return member



