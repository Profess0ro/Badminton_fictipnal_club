from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  
    path('articles/', views.ArticleList.as_view(), name='article_list'),
    path('article/<slug:slug>/', views.article_detail, name='article_detail'),
]