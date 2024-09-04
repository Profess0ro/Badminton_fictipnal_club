from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic, View
from .models import Article, Comment
from .forms import CommentForm
from django.contrib import messages


class ArticleList(generic.ListView):
    """
    Displays a paginated list of published articles on the home page.

    Attributes:
        model (Article): The model that this view will query.
        queryset (QuerySet): The QuerySet of published articles,
                             the articles are ordered by creation date.
        template_name (str): 'index.html' template are used to render
                             the list of articles.
        paginate_by (int): The number of articles to display per page.
    """
    model = Article
    queryset = Article.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'
    paginate_by = 6


class ArticleDetail(View):
    """
    Handles the display and comment submission for a single article.

    This view supports both GET and POST requests:
    - GET: Displays the article with its approved comments.
    - POST: Handles the submission of a new comment or
            the editing of an existing one.

    Methods:
        get(request, slug, *args, **kwargs):
        Renders the article detail page with comments.
        post(request, slug, *args, **kwargs):
        Processes a new comment or edits an existing one.

    Args:
        request (HttpRequest): The request object.
        slug (str): The slug of the article to be displayed.
    """
    def get(self, request, slug, *args, **kwargs):
        """
        Renders the article detail page with its comments.

        Args:
            request (HttpRequest): The request object.
            slug (str): The slug of the article to retrieve.

        Returns:
            HttpResponse: The rendered article detail page.
        """
        article = get_object_or_404(Article, slug=slug, status=1)
        comments = article.comments.filter(
            approved=True).order_by('created_on')
        comment_count = comments.count()
        comment_posted = request.GET.get('comment_posted', False)

        return render(
            request,
            "article_detail.html",
            {
                "article": article,
                "comments": comments,
                "comment_count": comment_count,
                "comment_form": CommentForm(),
                "comment_posted": comment_posted,
            },
        )

    def post(self, request, slug, *args, **kwargs):
        """
        Handles the submission of a new comment or editing an existing one.

        Args:
            request (HttpRequest): The request object.
            slug (str): The slug of the article to comment on.

        Returns:
            HttpResponse: Redirects to the article detail page on success,
            or re-renders the page if posting a comment was invalid.
        """
        article = get_object_or_404(Article, slug=slug, status=1)
        comments = article.comments.filter(
            approved=True).order_by('created_on')
        comment_count = comments.count()

        if 'edit_comment_content' in request.POST:
            comment_id = request.POST.get('comment_id')
            new_content = request.POST.get('edit_comment_content')
            comment = get_object_or_404(
                Comment, id=comment_id, author=request.user)
            comment.body = new_content
            comment.save()
            messages.success(request, "Comment updated successfully")
            return redirect('article_detail', slug=slug)

        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)
            comment.article = article
            comment.author = request.user
            comment.save()
            messages.success(request, "Comment posted successfully")

            return redirect(f'{request.path}?comment_posted=True')
        else:
            messages.error(
                request, "Failed to post comment. Please check the form.")
            return render(
                request,
                "article_detail.html",
                {
                    "article": article,
                    "comments": comments,
                    "comment_form": comment_form,
                    "comment_count": comment_count,
                    "comment_posted": False,
                },
            )


def edit_comment(request, comment_id):
    """
    Handles the editing of an existing comment.

    This view allows users to edit only
    their own comments on an article.
    When posting and the form is valid, the comment is updated;
    otherwise, the form is re-rendered with errors.

    Args:
        request (HttpRequest): The request object.
        comment_id (int): The ID of the comment to be edited.

    Returns:
        HttpResponse: Redirects to the article detail page on success,
        or re-renders the edit comment form with errors.
    """
    comment = get_object_or_404(Comment, id=comment_id)
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('article_detail', slug=comment.article.slug)
    else:
        form = CommentForm(instance=comment)

    return render(request, 'edit_comment.html', {'form': form})


def delete_comment(request, comment_id):
    """
    Handles the deletion of a comment by the user.

    This view allows users to delete their own comments.
    If the user is not the author of the comment,
    no delete button are visual.

    Args:
        request (HttpRequest): The request object.
        comment_id (int): The ID of the comment to be deleted.

    Returns:
        HttpResponse: Redirects to the article detail page.
    """
    if request.method == 'POST':
        comment = get_object_or_404(Comment, id=comment_id)
        article = get_object_or_404(Article, id=comment.article.id)

        if comment.author == request.user:
            comment.delete()
            messages.success(request, 'Comment deleted successfully.')
        else:
            messages.error(
                request, 'You do not have permission to delete this comment.')

        return redirect('article_detail', slug=article.slug)
    else:
        return redirect('article_detail', slug=article.slug)
