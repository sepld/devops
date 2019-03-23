from django.urls import path, include
from scripts import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('script', views.ScriptsViewSet)

urlpatterns = [
    path('', include(router.urls))
]
