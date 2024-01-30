from django.http import Http404, HttpRequest
from django.views.generic import DetailView
from django.views.generic.list import ListView
from django.urls import reverse
from django.shortcuts import render, redirect
from .forms import CommentForm
from .models import Article, ArticleCategory, ArticleComment


class ArticleListView(ListView):
    template_name = 'article_module/article_list.html'
    model = Article
    paginate_by = 3
    context_object_name = 'articles'

    def get_queryset(self):
        base_query = super().get_queryset()
        category_name = self.kwargs.get('category')
        if category_name is None:
            articles = base_query.filter(is_active=True)
            return articles
        else:
            articles = base_query.filter(categories__url_title__iexact=category_name, is_active=True)
            if articles:
                return articles
            raise Http404


def article_category_component(request):
    article_main_categories = \
        ArticleCategory.objects.prefetch_related('articlecategory_set').filter(is_active=True, parent=None)
    context = {'main_categories': article_main_categories}
    return render(request, 'article_module/components/article_category_component.html', context)


class ArticleDetailView(DetailView):
    template_name = 'article_module/article_detail.html'
    model = Article
    context_object_name = 'article'

    def get_queryset(self):
        base_query = super().get_queryset()
        article = base_query.filter(is_active=True)
        return article

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        article_id = self.kwargs.get('pk')
        context['comments'] = ArticleComment.objects.filter(
            article_id=article_id, parent=None).prefetch_related('articlecomment_set')
        context['form'] = CommentForm()
        return context

    def post(self, request, **kwargs):
        comment_form = CommentForm(request.POST)
        article_id = self.kwargs.get('pk')
        if comment_form.is_valid():
            comment = comment_form.cleaned_data.get('text')
            new_comment = ArticleComment(article_id=article_id, user_id=request.user.id, text=comment)
            new_comment.save()
            return redirect(reverse('article_detail_page', kwargs={'pk': article_id}))
        return redirect(reverse('article_detail_page', kwargs={'pk': article_id}))

