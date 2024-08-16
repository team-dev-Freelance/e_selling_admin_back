from rest_framework import serializers
from .models import Organisation


class OrganisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisation
        exclude = ['active']

    def validate_phone(self, value):
        """
        Validation personnalisée pour le champ `phone`.
        """
        if not value.startswith(('65', '67', '68', '69')):
            raise serializers.ValidationError('Le numéro doit commencer par 65, 67, 68 ou 69.')
        if len(value) != 9 or not value.isdigit():
            raise serializers.ValidationError('Le numéro de téléphone doit avoir 9 chiffres.')
        return value

