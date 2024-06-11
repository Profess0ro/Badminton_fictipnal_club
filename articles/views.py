from django.shortcuts import render 
from django.views import generic
from .models import Article

def index(request):
    return render(request, 'index.html')

class ArticleList(generic.ListView):
    model = Article
    queryset = Article.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'
    paginate_by = 6
