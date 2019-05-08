from django.urls import path, include
from rest_framework.routers import DefaultRouter
from vmware import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
# router.register(r'vcenter', views.VcenterViewSet)
# router.register(r'vm', views.VMViewSet)

urlpatterns = [
    path('', include(router.urls))
]
