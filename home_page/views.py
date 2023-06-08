from django.shortcuts import render
from board.models import Post, Category


def landing(request):
    return render(request,
                  'home_page/index.html',
                  {
                      'categories': Category.objects.all(),
                  })
