from django.shortcuts import render, get_object_or_404, redirect
from webapp.forms import ArticleForm
from webapp.models import Article
from django.views import View
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articles'] = Article.objects.all()
        return context


class ArticleView(TemplateView):
    template_name = 'article.html'

    def get_context_data(self, **kwargs):
        pk = kwargs.get('pk')
        context = super().get_context_data(**kwargs)
        context['article'] = get_object_or_404(Article, pk=pk)
        return context


class ArticleCreateView(View):
    def get(self, request, *args, **kwargs):
        form = ArticleForm()
        return render(request, 'create.html', context={'form': form})

    def post(self, request, *args, **kwargs):
        form = ArticleForm(data=request.POST)
        if form.is_valid():
            article = Article.objects.create(
                title=form.cleaned_data['title'],
                author=form.cleaned_data['author'],
                text=form.cleaned_data['text'],
                category=form.cleaned_data['category']
            )
            return redirect('article_view', pk=article.pk)
        else:
            return render(request, 'create.html', context={'form': form})


class ArticleUpdateView(View):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        article = get_object_or_404(Article, pk=pk)
        form = ArticleForm(data={
            'title': article.title,
            'text': article.text,
            'author': article.author,
            'category': article.category_id
        })
        return render(request, 'update.html', context={'form': form, 'article': article})

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        article = get_object_or_404(Article, pk=pk)
        form = ArticleForm(data=request.POST)
        if form.is_valid():
            data = form.cleaned_data
            article.title = data['title']
            article.text = data['text']
            article.author = data['author']
            article.category = data['category']
            article.save()
            return redirect('article_view', pk=article.pk)
        else:
            return render(request, 'update.html', context={'form': form, 'article': article})


class ArticleDeleteView(View):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        article = get_object_or_404(Article, pk=pk)
        return render(request, 'delete.html', context={'article': article})

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        article = get_object_or_404(Article, pk=pk)
        article.delete()
        return redirect('index')
