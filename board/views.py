from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import DetailView, CreateView, ListView, UpdateView
from django.db.models import Q
from .models import Post, Category, Comment
from .forms import CommentForm


class PostList(ListView):
    model = Post
    ordering = '-pk'


class PostUpdate(UpdateView):
    model = Post
    fields = ['title', 'content', 'head_image', 'category']

    template_name = 'board/post_update.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and self.get_object().author == request.user:
            return super(PostUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionError


class PostCreate(CreateView, LoginRequiredMixin):
    model = Post
    fields = ['title', 'content', 'head_image', 'category']

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated:
            form.instance.author = current_user
            return super(PostCreate, self).form_valid(form)
        else:
            return redirect('/')


class PostDetail(DetailView):
    model = Post

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostDetail, self).get_context_data()
        context['comment_form'] = CommentForm

        return context


class CategoryList(ListView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super(CategoryList, self).get_context_data()
        context['post_list'] = Post.objects.filter(category__slug=self.kwargs['slug']).order_by('-pk')
        context['category'] = Category.objects.get(slug=self.kwargs['slug'])

        return context


def add_comment(request, pk):
    if not request.user.is_authenticated:
        raise PermissionError

    if request.method == 'POST':
        post = Post.objects.get(pk=pk)
        comment_form = CommentForm(request.POST)
        comment_temp = comment_form.save(commit=False)
        comment_temp.post = post
        comment_temp.author = request.user
        comment_temp.save()

        return redirect(post.get_absolute_url())
    else:
        raise PermissionError


class CommentUpdate(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(CommentUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionError


class PostSearch(PostList):

    def get_queryset(self):
        q = self.kwargs['q']
        post_list = Post.objects.filter(
            Q(title__contains=q) | Q(content__contains=q) | Q(author__username__contains=q)
        ).distinct().order_by('-pk')
        return post_list

    def get_context_data(self, **kwargs):
        context = super(PostSearch, self).get_context_data()
        q = self.kwargs['q']
        context['search_info'] = f'검색어 {q}로 검색된 게시글 {self.get_queryset().count()}개'

        return context
