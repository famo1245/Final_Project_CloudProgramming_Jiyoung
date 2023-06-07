from django.shortcuts import render
from .models import Post


def landing(request):
    posts = Post.objects.all().order_by('-pk')

    return render(request,
                  'board/main.html',
                  {
                      'posts': posts,
                  })


def detail(request, pk):
    post = Post.objects.get(pk=pk)
    return render(request,
                  'board/post_detail.html',
                  {
                      'post': post,
                  })