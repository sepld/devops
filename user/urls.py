from django.urls import path, include
from rest_framework.routers import DefaultRouter
from user import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register('user', views.UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
