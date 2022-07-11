from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import *

from blog.forms import AddComent, RegisterUserForm, LoginUserForm, AddBlog
from blog.mixin import DataMixin
from blog.models import *


class Blog_home(DataMixin, TemplateView):
    template_name = 'blog/homepage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cont = self.get_user_context(title='Main page')
        return dict(list(context.items()) + list(cont.items()))


class Blogs_all(DataMixin, ListView):
    model = Blog
    template_name = 'blog/base.html'
    context_object_name = 'blogs'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cont = self.get_user_context(title='All blogs')
        return dict(list(context.items()) + list(cont.items()))


class Blog_add(DataMixin, CreateView):
    model = Blog
    form_class = AddBlog
    template_name = 'blog/add_blog.html'

    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        form.instance.is_published = True
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cont = self.get_user_context(title='Adding a new blog')
        return dict(list(context.items()) + list(cont.items()))


class Bloger_all(DataMixin, ListView):
    model = Bloger
    template_name = 'blog/base.html'
    context_object_name = 'bloggers'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cont = self.get_user_context(title='All bloggers',
                                     bloggers=Bloger.objects.exclude(Q(id=1) | Q(is_published=False)))
        return dict(list(context.items()) + list(cont.items()))


class Blog_show(DataMixin, DetailView):
    model = Blog
    template_name = 'blog/show_blog.html'
    context_object_name = 'blog'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cont = self.get_user_context(title=context['blog'],
                                     com=Comment.objects.filter(blog_id=context['blog'].id, is_published=True))
        return dict(list(context.items()) + list(cont.items()))


class BlogerView(DataMixin, ListView):
    model = Bloger
    template_name = 'blog/bloggerview.html'
    context_object_name = 'blogger'
    ordering = '-id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cont = self.get_user_context(title=Bloger.objects.get(slug=self.kwargs['slug']),
                                     blogger=Blog.objects.filter(author__slug=self.kwargs['slug']))
        return dict(list(context.items()) + list(cont.items()))


class CommentShow(DataMixin, CreateView):
    model = Comment
    form_class = AddComent
    template_name = 'blog/addcomment.html'

    def form_valid(self, form):
        form.instance.blog = get_object_or_404(Blog, slug=self.kwargs['slug'])
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cont = self.get_user_context(title='Comment for ' + str(get_object_or_404(Blog, slug=self.kwargs['slug'])))
        return dict(list(context.items()) + list(cont.items()))

class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'blog/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cont = self.get_user_context(title='New author registration')
        return dict(list(context.items()) + list(cont.items()))

    def form_valid(self, form):
        user = form.save(commit=False)
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        user = form.save()
        login(self.request, user)
        return redirect('home')


class Login(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'blog/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        con = self.get_user_context(title='Sign in')
        return dict(list(con.items()) + list(context.items()))

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')
