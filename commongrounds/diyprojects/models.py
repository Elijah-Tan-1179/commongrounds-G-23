from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class ProjectCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name_plural = "project categories"


class Project(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(ProjectCategory, on_delete=models.SET_NULL, null=True)
    creator = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    description = models.TextField()
    materials = models.TextField()
    steps = models.TextField()
    created_on = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_on']
        verbose_name_plural = "projects"


class Favorite(models.Model):
    project_status_choices = [
        ('B', 'Backlog'),
        ('T', 'To-Do'),
        ('D', 'Done')
    ]
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date_favorited = models.DateField()
    project_status = models.CharField(max_length=7, choices=project_status_choices)


class ProjectReview(models.Model):
    reviewer = models.ForeignKey(Profile, on_delete=models.CASCADE)
    comment = models.TextField()
    image = models.ImageField()


class ProjectRating(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    score = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )
