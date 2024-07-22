from django.urls import path
from . import views

urlpatterns = [
    path('', views.ArticleList.as_view(), name='index'), 
    path('<slug:slug>/', views.ArticleDetail.as_view(), name='article_detail'),
    path('edit_comment/<int:comment_id>/', views.edit_comment, name='edit_comment'),
    path('delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
]