from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=200, null=False, blank=False, verbose_name='Title')
    text = models.TextField(max_length=3000, null=False, blank=False, verbose_name='Text')
    author = models.CharField(max_length=40, null=False, blank=False, default='Unknown', verbose_name='Author')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    category = models.ForeignKey('Category', on_delete=models.PROTECT, null=True, blank=True, verbose_name='Category',
                                 related_name='articles')

    def __str__(self):
        return self.title


class Comment(models.Model):
    article = models.ForeignKey('webapp.Article', related_name='comments',
                                on_delete=models.CASCADE, verbose_name='Article')
    text = models.TextField(max_length=400, verbose_name='Comment')
    author = models.CharField(max_length=40, null=True, blank=True, default='Anonymous', verbose_name='Author')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')

    def __str__(self):
        return self.text[:20]


class Category(models.Model):
    name = models.CharField(max_length=20, verbose_name='Name')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
