"""
URL routing for API endpoints
"""
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter
from chemequip_backend.api.views import DatasetViewSet, UserViewSet, SummaryViewSet, EquipmentViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'datasets', DatasetViewSet, basename='dataset')
router.register(r'equipment', EquipmentViewSet, basename='equipment')
router.register(r'summary', SummaryViewSet, basename='summary')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls')),
    # Token authentication endpoints (used by desktop client)
    path('auth/token/login/', obtain_auth_token),
    path('api-token-auth/', obtain_auth_token),
]
