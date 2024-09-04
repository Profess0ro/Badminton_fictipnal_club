from .models import Comment
from django import forms


class CommentForm(forms.ModelForm):
    """
    A form for users to submit comments on a post.

    This form is linked to the `Comment` model and provides a way for users to
    enter and submit their comments.

    It uses Django's `ModelForm` to automatically
    generate form fields based on the `Comment` model,
    specifically the `content` field.

    The form is rendered in templates where users can write
    and post their comments.
    When submitting, the data is validated and saved to the database
    as a `Comment` instance.
    """
    class Meta:
        model = Comment
        fields = ('content',)
