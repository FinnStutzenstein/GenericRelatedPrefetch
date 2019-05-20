from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=255)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    def __str__(self):
        return self.name


class Book(models.Model):
    name = models.CharField(max_length=255)

    # Helper
    tags = GenericRelation(Tag)

    @property
    def tag(self):
        return self.tags.all()[0]

    def __str__(self):
        return self.name


class CD(models.Model):
    name = models.CharField(max_length=255)

    # Helper
    tags = GenericRelation(Tag)

    @property
    def tag(self):
        return self.tags.all()[0]

    def __str__(self):
        return self.name
