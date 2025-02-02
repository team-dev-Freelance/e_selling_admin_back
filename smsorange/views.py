from django.shortcuts import render

from django.http import JsonResponse

import requests
from django.conf import settings

def envoyer_sms(numero, message):
    """
    Envoie un SMS via l'API d'Orange Cameroun.
    """
    url_token = "https://api.orange.com/oauth/v3/token"
    url_sms = settings.ORANGE_SMS_API_URL.replace("tel%3A%2B237xxxxxxxxxx", f"tel%3A%2B{numero}")

    # Récupérer le token d'accès
    auth_response = requests.post(
        url_token,
        headers={
            'Authorization': f'Basic {settings.ORANGE_SMS_CLIENT_ID}:{settings.ORANGE_SMS_CLIENT_SECRET}'
        },
        data={
            'grant_type': 'client_credentials'
        }
    )

    if auth_response.status_code != 200:
        return "Erreur lors de l'obtention du token d'accès"

    access_token = auth_response.json().get('access_token')

    # Envoyer le SMS
    response = requests.post(
        url_sms,
        headers={
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json',
        },
        json={
            "outboundSMSMessageRequest": {
                "address": f"tel:+237{numero}",
                "senderAddress": "tel:+237xxxxxxxxxx",
                "outboundSMSTextMessage": {
                    "message": message
                }
            }
        }
    )

    if response.status_code == 201:
        return "SMS envoyé avec succès !"
    else:
        return f"Erreur lors de l'envoi du SMS : {response.text}"


def test_envoi_sms(request):
    numero = "672345678"  # Numéro de téléphone sans le préfixe +237
    message = "Bonjour ! Ce message a été envoyé via l'API Orange Cameroun."
    resultat = envoyer_sms(numero, message)
    return JsonResponse({'resultat': resultat})

