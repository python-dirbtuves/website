from .models import ParentComment

from .forms import ParentCommentForm


def get_model():
    return ParentComment


def get_form():
    return ParentCommentForm
