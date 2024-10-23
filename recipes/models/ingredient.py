from django.db import models


class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=50)  # e.g. cup, oz, lb, etc.

    def __str__(self):
        return self.name
