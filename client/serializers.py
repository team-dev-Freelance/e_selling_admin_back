from rest_framework import serializers

from rule.models import Role
from rule.serializers import RoleSerializer
from utilisateur.models import Client

from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
# from .models import Client


from rest_framework import serializers


class ClientSerializer(serializers.ModelSerializer):
    # rule = serializers.SerializerMethodField()
    # logo = serializers.SerializerMethodField()

    class Meta:
        model = Client
        # fields = ['id', 'username', 'email', 'phone', 'rule', 'logo', 'password', 'status', 'active']
        fields = ['id', "email" , "name" , "phone"  , "logo"]

   
    def get_logo(self, obj):
        # Si l'objet a un logo, renvoyer l'URL du fichier Cloudinary
        if obj.logo:
            try:
                # Si le champ logo est un objet Cloudinary, il doit avoir un attribut url
                return obj.logo.url
            except AttributeError:
                # Si logo est une chaîne (par ex. un chemin local ou un lien)
                return obj.logo  # Renvoie la chaîne telle quelle
        return None

    def validate_phone(self, value):
        """
        Validation personnalisée pour le champ `phone`.
        """
        if not value.startswith(('62', '67', '68', '69','65')):
            raise serializers.ValidationError('Le numéro doit commencer par 62,65, 67, 68 ou 69.')
        if len(value) != 9 or not value.isdigit():
            raise serializers.ValidationError('Le numéro de téléphone doit avoir 9 chiffres.')
        return value

    def create(self, validated_data):
        # Assurez-vous que le mot de passe est fourni dans les données validées
        password = validated_data.pop('password', None)
        client = super().create(validated_data)
        if password:
            client.set_password(password)
            client.save()
        return client
    
    def validate_email(self, value):
        # Validate email format
        email_validator = EmailValidator()
        try:
            email_validator(value)
        except ValidationError:
            raise serializers.ValidationError('Email format is invalid.')
        return value

    def validate_password(self, value):
        # Check password length
        if len(value) < 5:  # Example: password needs to be at least 5 characters
            raise serializers.ValidationError('Le mot de passe doit contenir au moins 4 caractères.')

    def validate(self, data):
        errors = []
        
        if 'name' not in data or not data['name']:
            errors.append({
                'message': 'Ce champ est obligatoire.',
                'statut': 'error',
                'champ': 'name'
            })
            
        if 'email' not in data or not data['email']:
            errors.append({
                'message': 'Ce champ est obligatoire.',
                'statut': 'error',
                'champ': 'email'
            })
            
        if 'phone' not in data or not data['phone']:
            errors.append({
                    'message': 'Ce champ est obligatoire.',
                    'statut': 'error',
                    'champ': 'phone'
                })
            
        
            
        if errors:
            raise serializers.ValidationError(errors)

        return data