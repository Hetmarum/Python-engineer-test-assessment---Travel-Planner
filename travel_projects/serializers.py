import requests
from django.db import IntegrityError
from rest_framework import serializers
from travel_projects.models import TravelProject, ProjectPlace
from travel_projects.utils import fetch_artwork


class ProjectPlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectPlace
        fields = [
            "id",
            "external_id",
            "title",
            "notes",
            "visited",
        ]
        read_only_fields = ["title"]

    def validate_external_id(self, value):
        """
        Validate artwork exists in Art Institute API.
        """
        artwork = fetch_artwork(value)
        if not artwork:
            raise serializers.ValidationError("Artwork not found in Art Institute API.")

        self.context["artwork_data"] = artwork
        return value

    def validate(self, attrs):
        project = self.context.get("project")

        if self.instance is None:
            if project.places.count() >= 10:
                raise serializers.ValidationError(
                    "Maximum 10 places allowed per project."
                )

        return attrs

    def create(self, validated_data):
        project = self.context["project"]
        artwork = self.context.get("artwork_data")

        try:
            place = ProjectPlace.objects.create(
                project=project,
                external_id=validated_data["external_id"],
                title=artwork.get("title", "Unknown"),
            )
        except IntegrityError:
            raise serializers.ValidationError(
                "This artwork is already added to this project."
            )

        return place

    def update(self, instance, validated_data):
        instance.notes = validated_data.get("notes", instance.notes)
        instance.visited = validated_data.get("visited", instance.visited)
        instance.save()

        instance.project.update_completion_status()

        return instance


class PlaceInputSerializer(serializers.Serializer):
    external_id = serializers.IntegerField()


class TravelProjectSerializer(serializers.ModelSerializer):
    places = ProjectPlaceSerializer(many=True, read_only=True)
    places_input = PlaceInputSerializer(many=True, write_only=True, required=False)

    class Meta:
        model = TravelProject
        fields = [
            "id",
            "name",
            "description",
            "start_date",
            "completed",
            "places",
            "places_input",
        ]
        read_only_fields = ["completed"]

    def create(self, validated_data):
        places_data = validated_data.pop("places_input", [])

        project = TravelProject.objects.create(**validated_data)

        if len(places_data) > 10:
            raise serializers.ValidationError("Maximum 10 places allowed per project.")

        for place in places_data:
            artwork = fetch_artwork(place["external_id"])

            if not artwork:
                raise serializers.ValidationError(
                    f"Artwork with id {place['external_id']} not found."
                )

            ProjectPlace.objects.create(
                project=project,
                external_id=place["external_id"],
                title=artwork.get("title", "Unknown"),
            )

        return project
