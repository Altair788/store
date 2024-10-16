from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied
from django.forms import inlineformset_factory
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from catalog.forms import ProductForm, VersionForm
from catalog.models import Product, Version
from configs import FEEDBACKS_PATH
from utils import write_to_file


class ProductListView(ListView):
    model = Product


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    success_url = reverse_lazy('catalog:catalog/product_list')
    form_class = ProductForm

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        ProductFormset = inlineformset_factory(
            Product, Version, VersionForm, extra=1
        )
        if self.request.method == "POST":
            context_data["formset"] = ProductFormset(
                self.request.POST, instance=self.object
            )
        else:
            context_data["formset"] = ProductFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        product = form.save()
        user = self.request.user
        product.owner = user
        product.save()

        context_data = self.get_context_data()
        formset = context_data["formset"]
        if form.is_valid() and formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)

        else:
            return self.render_to_response(
                self.get_context_data(form=form, formset=formset)
            )


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    success_url = reverse_lazy('catalog:catalog/product_list')
    form_class = ProductForm
    permission_required = ('catalog.set_published', 'catalog.change_product',)

    def get_success_url(self):
        return reverse("catalog:catalog/product_detail", args=[self.kwargs.get("pk")])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        ProductFormset = inlineformset_factory(
            Product, Version, VersionForm, extra=1
        )
        if self.request.method == "POST":
            context_data["formset"] = ProductFormset(
                self.request.POST, instance=self.object
            )
        else:
            context_data["formset"] = ProductFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data["formset"]
        if form.is_valid() and formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)

        else:
            return self.render_to_response(
                self.get_context_data(form=form, formset=formset)
            )

    # если хотим оставить
    # def has_permission(self):
    #     self.object = self.get_object()
    #     user = self.request.user
    #     # Проверяем наличие хотя бы одного из разрешений
    #     return user == self.object.owner or user.has_perms(self.permission_required)

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        user = self.request.user
        if user == self.object.owner or user.has_perm('catalog.change_product'):
            return self.object
        else:
            raise PermissionDenied




class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:catalog/product_list')


class ContactView(View):
    template_name = 'catalog/contact.html'

    def get(self, request):
        return render(request, self.template_name)

    @staticmethod
    def post(request):
        feedback_dict = {}
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")
        print(f"New message from {name} ({phone}): {message}")

        feedback_dict["name"] = name
        feedback_dict["phone"] = phone
        feedback_dict["message"] = message

        write_to_file(feedback_dict, FEEDBACKS_PATH)
        print("Обращение записано.")

        return redirect(reverse_lazy('catalog:catalog/contact'))


class CatalogProtectedView(LoginRequiredMixin, View):
    login_url = "login/"  # URL для страницы входа
    redirect_field_name = "next"  # Параметр для возврата на предыдущую страницу после входа

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect_to_login(
                self.request.get_full_path(),
                settings.LOGIN_URL,
                self.redirect_field_name)

        return super().dispatch(request, *args, **kwargs)
