


import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Role
from .forms import RoleForm
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .serializers import RoleSerializer
# Liste des catégories
@require_http_methods(["GET"])
def role_list(request):
    roles = Role.objects.all()
    
    # Sérialiser les catégories
    serializer = RoleSerializer(roles, many=True)  
    return JsonResponse({
        'response': serializer.data  
    }, status=200)  # 200 OK

@csrf_exempt
def role_delete(request, pk):
     
    role = get_object_or_404(Role, pk=pk)
    role.delete()
    return JsonResponse({
        'status': 'success',
        'message': 'Role supprimé avec succès.'
    }, status=204)  # 204 No Content
@csrf_exempt
def role_update(request, pk):
    
    if request.body:
        data = json.loads(request.body)
       
        item = get_object_or_404(Role, pk=pk)
       


        # Vérification si le role existe déjà 
        if Role.objects.filter(role=data['role']).exclude(pk=item.pk).exists():
            return JsonResponse({
                'status': 'error',
                'message': 'Ce role existe déjà.'
            }, status=400)  # 400 Bad Request


        form = RoleForm(data, instance=item)
        if form.is_valid():
            item = form.save()
            return JsonResponse({
                'status': 'success',
                'message': 'Role mis à jour avec succès.',
                'data': {
                    'role': item.role,
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

@csrf_exempt
@require_http_methods(["POST"])
def role_create(request):

    if request.body:
        
        data = json.loads(request.body)
        role = data.get("role")
        

        # Vérification de l'existence
        if Role.objects.filter(role=role).exists():
            return JsonResponse({
                'status': 'error',
                'message': 'Ce role existe déjà.'
            }, status=400)  # 400 Bad Request

        # Créer la catégorie
        form = RoleForm(data)
        if form.is_valid():
            item = form.save()
            return JsonResponse({
                'status': 'success',
                'message': 'Catégorie créée avec succès.',
                'data': {
                    'label': item.role,
                    # 'description': RoleForm.description,
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

