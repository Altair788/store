from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import redirect_to_login
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from pytils.translit import slugify

from blog.models import Article
from blog.tasks import send_notification_email


class ArticleCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Article
    fields = (
        'title',
        'body',
        'preview',
    )
    success_url = reverse_lazy('blog:article_list')
    permission_required = 'blog.add_article'

    def form_valid(self, form):
        form.instance.slug = slugify(form.instance.title)

        return super().form_valid(form)


class ArticleUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Article
    fields = (
        'title',
        'body',
        'preview',
    )
    permission_required = 'blog.change_article'

    def form_valid(self, form):
        form.instance.slug = slugify(form.instance.title)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:article_detail', args=[self.kwargs.get('pk')])


class ArticleListView(PermissionRequiredMixin, ListView):
    model = Article
    permission_required = 'blog.view_article'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not context['object_list']:
            context['message'] = ('В настоящее время мы готовим для вас новые публикации'
                                  ' с результатами проведенных исследований.')
        return context


class ArticleDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Article
    permission_required = 'blog.view_article'
    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_counter += 1
        self.object.save()

        if self.object.views_counter == 25:
            send_notification_email(self.object.title, self.object.views_counter)

        return self.object


class ArticleDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Article
    success_url = reverse_lazy('blog:article_list')
    permission_required = 'blog.delete_article'




class BlogProtectedView(LoginRequiredMixin, View):
    login_url = "login/"  # URL для страницы входа
    redirect_field_name = "next"  # Параметр для возврата на предыдущую страницу после входа

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect_to_login(
                self.request.get_full_path(),
                settings.LOGIN_URL,
                self.redirect_field_name)

        return super().dispatch(request, *args, **kwargs)