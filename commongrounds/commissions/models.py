from django.db import models

# Model containing commission TYPE
class CommissionType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

# Model containing the commission REQUEST
class Commission(models.Model):

    title = models.CharField(max_length=255)
    description = models.TextField()
    people_required = models.PositiveIntegerField()

    # Created on and updated on req
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_on"]

    def __str__(self):
        return self.title