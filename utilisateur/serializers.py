from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from rest_framework import serializers
import logging

logger = logging.getLogger(__name__)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        # Authentifier l'utilisateur
        user = authenticate(request=self.context.get('request'), username=username, password=password)

        logger.debug(f'Authenticating user: {username}, User object: {user}')

        if user is None:
            logger.error('User authentication failed')
            raise serializers.ValidationError({"detail": "Invalid credentials"})

        attrs['user'] = user
        data = super().validate(attrs)
        data['rule'] = user.rule.role

        if hasattr(user, 'member'):
            data['organisation_id'] = user.member.organisation.id

        if user.logo:
            data['logo'] = user.logo.url

        return data
