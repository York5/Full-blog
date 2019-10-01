from django.shortcuts import render, get_object_or_404, redirect
from webapp.forms import ArticleForm, CommentForm
from webapp.models import Article, Comment
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


class CommentIndexView(TemplateView):
    template_name = 'comments/comment_index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.order_by('-created_at')
        return context


class CommentView(TemplateView):
    template_name = 'comments/comment.html'

    def get_context_data(self, **kwargs):
        pk = kwargs.get('pk')
        context = super().get_context_data(**kwargs)
        context['comment'] = get_object_or_404(Comment, pk=pk)
        return context


class CommentCreateView(View):
    def get(self, request, *args, **kwargs):
        if request.method == 'GET':
            form = CommentForm()
            return render(request, 'comments/comment_create.html', context={'form': form})

    def post(self, request, *args, **kwargs):
        form = CommentForm(data=request.POST)
        if form.is_valid():
            comment = Comment.objects.create(
                article=form.cleaned_data['article'],
                text=form.cleaned_data['text'],
                author=form.cleaned_data['author']
                )
            return redirect('comment_view', pk=comment.pk)
        else:
            return render(request, 'comments/comment_create.html', context={'form': form})


class CommentUpdateView(View):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        comment = get_object_or_404(Comment, pk=pk)
        form = CommentForm(data={
            'article': comment.article,
            'text': comment.text,
            'author': comment.author
            })
        return render(request, 'comments/comment_update.html', context={'form': form, 'comment': comment})

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        comment = get_object_or_404(Comment, pk=pk)
        form = CommentForm(data=request.POST)
        if form.is_valid():
            data = form.cleaned_data
            comment.text = data['text'],
            comment.author = data['author'],
            comment.save()
            return redirect('comment_view', pk=comment.pk)
        else:
            return render(request, 'comments/comment_update.html', context={'form': form, 'comment': comment})


class CommentDeleteView(View):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        comment = get_object_or_404(Comment, pk=pk)
        return render(request, 'comments/comment_delete.html', context={'comment': comment})

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        comment = get_object_or_404(Comment, pk=pk)
        comment.delete()
        return redirect('comment_index')
