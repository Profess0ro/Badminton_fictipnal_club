from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic, View
from .models import Article, Comment
from .forms import CommentForm
from django.contrib import messages

class ArticleList(generic.ListView):
    model = Article
    queryset = Article.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'
    paginate_by = 6

class ArticleDetail(View):
    def get(self, request, slug, *args, **kwargs):
        article = get_object_or_404(Article, slug=slug, status=1)
        comments = article.comments.filter(approved=True).order_by('created_on')
        return render(
            request,
            "article_detail.html",
            {
                "article": article,
                "comments": comments,
                "commented": False,
                "comment_form": CommentForm()
            },
        )

    def post(self, request, slug, *args, **kwargs):
        article = get_object_or_404(Article, slug=slug, status=1)
        comments = article.comments.filter(approved=True).order_by('created_on')

        if 'edit_comment_content' in request.POST:
            comment_id = request.POST.get('comment_id')
            new_content = request.POST.get('edit_comment_content')
            comment = get_object_or_404(Comment, id=comment_id, author=request.user)
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
            return redirect('article_detail', slug=slug)
        else:
            messages.error(request, "Failed to post comment. Please check the form.")
            return render(
                request,
                "article_detail.html",
                {
                    "article": article,
                    "comments": comments,
                    "commented": False,
                    "comment_form": comment_form
                },
            )

def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('article_detail', slug=comment.article.slug)  
    else:
        form = CommentForm(instance=comment)
    
    return render(request, 'edit_comment.html', {'form': form})

def delete_comment(request, slug, comment_id):
    if request.method == 'POST':
        comment = get_object_or_404(Comment, id=comment_id)
        article = get_object_or_404(Article, slug=slug)
        comment.delete()
        messages.success(request, 'Comment deleted successfully.')
        return redirect('article_detail', slug=article.slug)
    else:
        return redirect('article_detail', slug=slug)