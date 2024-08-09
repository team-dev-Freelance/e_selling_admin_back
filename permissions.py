from rest_framework import permissions


class IsAdminOrUser(permissions.BasePermission):
    """
    Permission pour vérifier si le membre est Admin ou User
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.rule.role in ['ADMIN', 'USER']


class IsAdmin(permissions.BasePermission):
    """
    Permission pour vérifier si le membre est Admin
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.rule.role == 'ADMIN'


class IsMemberOrUser(permissions.BasePermission):
    """
    Permission pour vérifier si le membre est Member ou User
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.rule.role in ['MEMBER', 'USER']


class IsUser(permissions.BasePermission):
    """
    Permission pour vérifier si le membre est User
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.rule.role == 'USER'


class IsMember(permissions.BasePermission):
    """
    Permission pour vérifier si le membre est Member
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.rule.role == 'MEMBER'


class IsCreatorOrReadOnly(permissions.BasePermission):
    """
    Permission pour vérifier si l'utilisateur est le créateur de l'article
    """

    def has_object_permission(self, request, view, obj):
        # Les permissions sont uniquement accordées au créateur de l'article
        return obj.member == request.user


class IsMemberOfOrganisation(permissions.BasePermission):
    """
    Permission pour vérifier si l'utilisateur est un membre de l'organisation
    """

    def has_object_permission(self, request, view, obj):
        # Les permissions sont uniquement accordées aux membres de l'organisation
        return obj.members.filter(id=request.user.id).exists()


class IsMemberUserOfOrganisation(permissions.BasePermission):
    """
    Permission pour vérifier si l'utilisateur est un membre de l'organisation
    """

    def has_object_permission(self, request, view, obj):
        # Les permissions sont uniquement accordées aux membres de l'organisation
        return obj.members.filter(id=request.user.id, role__role='USER').exists()


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the object.
        return obj.client == request.user
