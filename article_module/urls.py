from django.urls import path
from . import views


urlpatterns = [
    path('', views.ArticleListView.as_view(), name='article_list_page'),
    path('cat/<str:category>', views.ArticleListView.as_view(), name='article_by_category_list_page'),
    path('<int:pk>', views.ArticleDetailView.as_view(), name='article_detail_page'),

]
