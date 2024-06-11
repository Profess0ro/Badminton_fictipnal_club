from django.shortcuts import render, get_object_or_404 
from django.views import generic
from .models import Article

def index(request):
    articles = Article.objects.all().order_by('-created_on')
    context = {
        'article_list': articles,
    }
    
    return render(request, 'index.html', context)

def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug)
    return render(request, 'article_detail.html', {'article': article})

class ArticleList(generic.ListView):
    model = Article
    queryset = Article.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'
    paginate_by = 6
