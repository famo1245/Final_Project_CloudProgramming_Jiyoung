from django.shortcuts import render
from .models import Post, Category


def landing(request):
    post_list = Post.objects.all().order_by('-pk')

    return render(request,
                  'board/main.html',
                  {
                      'post_list': post_list,
                  })


def detail(request, pk):
    post = Post.objects.get(pk=pk)
    return render(request,
                  'board/post_detail.html',
                  {
                      'post': post,
                  })


def category_page(request, slug):
    category = Category.objects.get(slug=slug)
    post_list = Post.objects.filter(category=category).order_by('-pk')

    return render(request,
                  'board/main.html',
                  {
                      'category': category,
                      'post_list': post_list,
                  })
