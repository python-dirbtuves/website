from django.db import models
from django_comments.models import Comment


class ParentComment(Comment):
    parent_comment = models.ForeignKey('self', null=True, blank=True)
