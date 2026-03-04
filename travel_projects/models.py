from django.db import models


class TravelProject(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    start_date = models.DateField(blank=True, null=True)
    completed = models.BooleanField(default=False)

    def update_completion_status(self):
        if self.places.exists() and not self.places.filter(visited=False).exists():
            self.completed = True
        else:
            self.completed = False

        self.save(update_fields=["completed"])

    def __str__(self):
        return self.name


class ProjectPlace(models.Model):
    project = models.ForeignKey(
        TravelProject, related_name="places", on_delete=models.CASCADE
    )
    external_id = models.IntegerField()
    title = models.CharField(max_length=255)
    notes = models.TextField(blank=True)
    visited = models.BooleanField(default=False)

    class Meta:
        unique_together = ("project", "external_id")
