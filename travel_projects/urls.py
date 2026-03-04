"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from .views import TravelProjectViewSet, ProjectPlaceViewSet

router = DefaultRouter()
router.register(r"projects", TravelProjectViewSet, basename="projects")

urlpatterns = [
    path("", include(router.urls)),
    path(
        "projects/<int:project_id>/places/",
        ProjectPlaceViewSet.as_view(
            {
                "get": "list",
                "post": "create",
            }
        ),
        name="project-places-list",
    ),
    path(
        "projects/<int:project_id>/places/<int:pk>/",
        ProjectPlaceViewSet.as_view(
            {
                "get": "retrieve",
                "patch": "partial_update",
                "put": "update",
                "delete": "destroy",
            }
        ),
        name="project-places-detail",
    ),
]
