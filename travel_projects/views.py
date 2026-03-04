from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from django.shortcuts import get_object_or_404

from travel_projects.models import TravelProject, ProjectPlace
from travel_projects.serializers import TravelProjectSerializer, ProjectPlaceSerializer


class TravelProjectViewSet(viewsets.ModelViewSet):
    queryset = TravelProject.objects.all().order_by("-id")
    serializer_class = TravelProjectSerializer

    def destroy(self, request, *args, **kwargs):
        project = self.get_object()

        if project.places.filter(visited=True).exists():
            return Response(
                {"detail": "Cannot delete project with visited places."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return super().destroy(request, *args, **kwargs)


class ProjectPlaceViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectPlaceSerializer

    def get_project(self):
        project_id = self.kwargs.get("project_id")
        return get_object_or_404(TravelProject, id=project_id)

    def get_queryset(self):
        project = self.get_project()
        return project.places.all().order_by("-id")

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["project"] = self.get_project()
        return context

    def create(self, request, *args, **kwargs):
        project = self.get_project()

        if project.places.count() >= 10:
            return Response(
                {"detail": "Maximum 10 places allowed per project."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return super().create(request, *args, **kwargs)
