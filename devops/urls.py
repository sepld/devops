"""devops URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from user.urls import router as user_router
from servers.urls import router as servers_router
from scripts.urls import router as scripts_router
from public.utils.component import merge_list

router = DefaultRouter()

router.registry = merge_list(
    user_router.registry,
    servers_router.registry,
    scripts_router.registry
)

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('', include(router.urls)),
    path('user/', include('user.urls')),
    path('servers/', include('servers.urls'))

]
