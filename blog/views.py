from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from pytils.translit import slugify

from blog.models import Article
from blog.tasks import send_notification_email


class ArticleCreateView(CreateView):
    model = Article
    fields = (
        'title',
        'body',
        'preview',
    )
    success_url = reverse_lazy('blog:article_list')

    def form_valid(self, form):
        form.instance.slug = slugify(form.instance.title)

        return super().form_valid(form)


class ArticleUpdateView(UpdateView):
    model = Article
    fields = (
        'title',
        'body',
        'preview',
    )

    def form_valid(self, form):
        form.instance.slug = slugify(form.instance.title)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:article_detail', args=[self.kwargs.get('pk')])


class ArticleListView(ListView):
    model = Article

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


class ArticleDetailView(DetailView):
    model = Article

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_counter += 1
        self.object.save()

        if self.object.views_counter == 25:
            send_notification_email(self.object.title, self.object.views_counter)

        return self.object


class ArticleDeleteView(DeleteView):
    model = Article
    success_url = reverse_lazy('blog:article_list')
