from django.urls import path, include
from servers import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('server', views.ServersViewSet)

urlpatterns = [
    path('', include(router.urls))
]
