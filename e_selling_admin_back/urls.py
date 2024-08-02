"""
URL configuration for e_selling_admin_back project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from acheter.views import AcheterViewSet
from member.views import MemberViewSet
from organisation.views import OrganisationViewSet
from rule.views import RoleViewSet
from privilegies.views import PrivilegiesViewSet
from article.views import ArticleViewSet
from client.views import ClientViewSet
from categorie.views import CategoriesViewSet

#from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


router = DefaultRouter()
router.register(r'member', MemberViewSet)
router.register(r'organisation', OrganisationViewSet)
router.register(r'rule', RoleViewSet)
router.register(r'privilegies', PrivilegiesViewSet)
router.register(r'article', ArticleViewSet)
router.register(r'client', ClientViewSet)
router.register(r'categorie', CategoriesViewSet)
router.register(r'acheter', AcheterViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    #path('api/', include('member.urls')),
    #path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    #path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
