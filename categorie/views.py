


import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Categorie
from .forms import CategorieForm
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .serializers import CategorieSerializer
# Liste des catégories
@require_http_methods(["GET"])
def categorie_list(request):
    categories = Categorie.objects.all()
    
    # Sérialiser les catégories
    serializer = CategorieSerializer(categories, many=True)  
    return JsonResponse({
        'response': serializer.data  
    }, status=200)  # 200 OK

# Créer une nouvelle catégorie avec vérification d'existence
@csrf_exempt
@require_http_methods(["GET"])
def categorie_create(request):

    if request.body:
        
        data = json.loads(request.body)
        label = data.get("label")
        

        # Vérification de l'existence
        if Categorie.objects.filter(label=label).exists():
            return JsonResponse({
                'status': 'error',
                'message': 'Une catégorie avec ce label existe déjà.'
            }, status=400)  # 400 Bad Request

        # Créer la catégorie
        # form = CategorieForm(data)
        # if form.is_valid():
            categorie = form.save()
            return JsonResponse({
                'status': 'success',
                'message': 'Catégorie créée avec succès.',
                'data': {
                    'label': categorie.label,
                    # 'description': categorie.description,
                }
            }, status=201)  # 201 Created
        
        return JsonResponse({
            'status': 'error',
            'message': 'Les données fournies sont invalides.',
            'errors': form.errors,
        }, status=400)  # 400 Bad Request

    return JsonResponse({
        'status': 'error',
        'message': 'Aucune donnée fournie.'
    }, status=400)  # 400 Bad Request

# Mettre à jour une catégorie existante
@csrf_exempt
def categorie_update(request, pk):
   
    if request.body:
        data = json.loads(request.body)
        
        categorie = get_object_or_404(Categorie, pk=pk)

        # Vérification si le label existe déjà dans une autre catégorie
        if 'label' in data and Categorie.objects.filter(label=data['label']).exclude(pk=categorie.pk).exists():
            return JsonResponse({
                'status': 'error',
                'message': 'Une catégorie avec ce label existe déjà.'
            }, status=400)  # 400 Bad Request

        form = CategorieForm(data, instance=categorie)
        if form.is_valid():
            categorie = form.save()
            return JsonResponse({
                'status': 'success',
                'message': 'Catégorie mise à jour avec succès.',
                'data': {
                    'label': categorie.label,
                }
            }, status=200)  # 200 OK
        return JsonResponse({
            'status': 'error',
            'message': 'Les données fournies sont invalides.',
            'errors': form.errors,
        }, status=400)  # 400 Bad Request

    return JsonResponse({
        'status': 'error',
        'message': 'Aucune donnée fournie.'
    }, status=400)  # 400 Bad Request

@require_http_methods(["GET"])
def categorie_detail(request, pk):
    # Récupérer la catégorie par son ID
    categorie = get_object_or_404(Categorie, id=pk)
    
    # Sérialiser la catégorie
    serializer = CategorieSerializer(categorie)

    return JsonResponse({
        'response': serializer.data  
    }, status=200)  # 200 OK
# # Supprimer une catégorie
# @require_http_methods(["DELETE"])
@csrf_exempt
def categorie_delete(request, pk):
     
    categorie = get_object_or_404(Categorie, pk=pk)
    categorie.delete()
    return JsonResponse({
        'status': 'success',
        'message': 'Catégorie supprimée avec succès.'
    }, status=204)  # 204 No Content