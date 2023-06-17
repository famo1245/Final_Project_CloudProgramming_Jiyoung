from django.shortcuts import render
from board.models import Post, Category


def landing(request):
    duo_list = Post.objects.filter(category__slug='듀오').order_by('-pk')[:5]
    squad_list = Post.objects.filter(category__slug='스쿼드').order_by('-pk')[:5]
    free_list = Post.objects.filter(category__slug='자유').order_by('-pk')[:5]
    return render(request,
                  'home_page/index.html',
                  {
                      'duo_list': duo_list,
                      'squad_list': squad_list,
                      'free_list': free_list,
                  })
