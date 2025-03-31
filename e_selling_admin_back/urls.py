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
from cart.views import CartView
# from cart.views import CartViewSet
# from cart.views import CartView
# from cart.views import CartDetailView
from categorie.views import CategoriesViewSet
from client.views import ClientViewSet
from e_selling_admin_back import settings
from member.views import MemberViewSet
from order.views import PasserCommandeView, OrderHistoryView, OrderListByOrganizationView
# from order.views import OrderViewSet, PasserCommandeView
from organisation.views import OrganisationViewSet
from passwordResetCode.views import SendPasswordResetCodeView, VerifyResetCodeView
from privilegies.views import PrivilegiesViewSet
from rule.views import RoleViewSet
# from smsorange.views import test_envoi_sms
from utilisateur.views import MyTokenObtainPairView, LogoutView, ChangePasswordView, CurrentUserView, \
    ResendPasswordResetCodeView, ResetPasswordView, CurrentClientView, UpdateClientView

from organisation import views as organisationView
router = DefaultRouter()
router.register(r'member', MemberViewSet)
router.register(r'organisation', OrganisationViewSet)
router.register(r'rule', RoleViewSet)
router.register(r'privilegies', PrivilegiesViewSet)
router.register(r'article', ArticleViewSet)
router.register(r'client', ClientViewSet)
router.register(r'categorie', CategoriesViewSet)
# router.register(r'orders', OrderViewSet, basename='order')
# router.register(r'acheter', AcheterViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset_password'),
    path('send-reset-code/', SendPasswordResetCodeView.as_view(), name='send_reset_code'),
    path('verify-reset-code/', VerifyResetCodeView.as_view(), name='verify_reset_code'),
    path('resend-code/', ResendPasswordResetCodeView.as_view(), name='resend_code'),
    path('current-user/', CurrentUserView.as_view(), name='current_user'),
    path('current-client/', CurrentClientView.as_view(), name='current_client'),
    path('client/<int:pk>/', UpdateClientView.as_view(), name='update_client'),
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/<int:item_id>/', CartView.as_view(), name='cart-item-delete'),
    path('cart/passer_commande/', PasserCommandeView.as_view(), name='passer_commande'),
    path('order-history/', OrderHistoryView.as_view(), name='order-history'),
    path('orders/organization/', OrderListByOrganizationView.as_view(), name='orders-by-organization'),
    # path('test-sms/', test_envoi_sms, name='test_envoi_sms'),
    # path('admin/', admin.site.urls),
    # path('sms/', include('sms_app.urls')),
    path('get-image', organisationView.serve_image),
    path('user/', include('utilisateur.urls')),

    path('', include(router.urls)),
]

# Ajoutez les configurations pour les fichiers médias si en mode développement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


