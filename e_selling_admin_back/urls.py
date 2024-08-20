from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# from acheter.views import AcheterViewSet
from article.views import ArticleViewSet
from cart.views import CartViewSet
# from cart.views import CartViewSet
# from cart.views import CartView
# from cart.views import CartDetailView
from categorie.views import CategoriesViewSet
from client.views import ClientViewSet
from e_selling_admin_back import settings
from member.views import MemberViewSet
from organisation.views import OrganisationViewSet
from passwordResetCode.views import SendPasswordResetCodeView, VerifyResetCodeView
from privilegies.views import PrivilegiesViewSet
from rule.views import RoleViewSet
from utilisateur.views import MyTokenObtainPairView, LogoutView, ChangePasswordView, CurrentUserView, \
    ResendPasswordResetCodeView

router = DefaultRouter()
router.register(r'member', MemberViewSet)
router.register(r'organisation', OrganisationViewSet)
router.register(r'rule', RoleViewSet)
router.register(r'privilegies', PrivilegiesViewSet)
router.register(r'article', ArticleViewSet)
router.register(r'client', ClientViewSet)
router.register(r'categorie', CategoriesViewSet)
# router.register(r'acheter', AcheterViewSet)
router.register('cart', CartViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    # path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('send-reset-code/', SendPasswordResetCodeView.as_view(), name='send_reset_code'),
    path('verify-reset-code/', VerifyResetCodeView.as_view(), name='verify_reset_code'),
    path('resend-code/', ResendPasswordResetCodeView.as_view(), name='resend_code'),
    path('current-user/', CurrentUserView.as_view(), name='current_user'),
]

# Ajoutez les configurations pour les fichiers médias si en mode développement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


