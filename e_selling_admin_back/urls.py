from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from acheter.views import AcheterViewSet
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
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

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

