from django_comments.forms import CommentForm
from .models import ParentComment


class ParentCommentForm(CommentForm):

    def get_comment_model(self):
        return ParentComment
