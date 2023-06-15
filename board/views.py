from django.shortcuts import render
from django.views.generic import DetailView, CreateView, ListView
from .models import Post, Category
from .forms import CommentForm


class PostList(ListView):
    model = Post
    ordering = '-pk'


class PostCreate(CreateView):
    model = Post
    fields = ['title', 'content', 'head_image', 'category']


class PostDetail(DetailView):
    model = Post

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostDetail, self).get_context_data()
        context['comment_form'] = CommentForm

        return context


class CategoryList(ListView):
    model = Post
    ordering = '-pk'

    def get_context_data(self, **kwargs):
        context = super(CategoryList, self).get_context_data()
        context['post_list'] = Post.objects.filter(category__slug=self.kwargs['slug'])
        context['category'] = Category.objects.get(slug=self.kwargs['slug'])

        return context


def category_page(request, slug):
    category = Category.objects.get(slug=slug)
    post_list = Post.objects.filter(category=category).order_by('-pk')

    return render(request,
                  'board/post_list.html',
                  {
                      'category': category,
                      'post_list': post_list,
                  })
