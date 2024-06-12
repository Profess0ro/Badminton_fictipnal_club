from django.urls import path
from . import views

urlpatterns = [
    path('', views.ArticleList.as_view(), name='index'), 
    path('<slug:slug>/', views.ArticleDetail.as_view(), name='article_detail'), 
    # path('articles/', views.ArticleList.as_view(), name='article_list'),
    # path('article/<slug:slug>/', views.article_detail, name='article_detail'),
]