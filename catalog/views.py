from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from catalog.forms import ProductForm
from catalog.models import Product
from configs import FEEDBACKS_PATH
from utils import write_to_file


class ProductListView(ListView):
    model = Product


class ProductDetailView(DetailView):
    model = Product



class ProductCreateView(CreateView):
    model = Product
    success_url = reverse_lazy('catalog:catalog/product_list')
    form_class = ProductForm

class ProductUpdateView(UpdateView):
    model = Product
    success_url = reverse_lazy('catalog:catalog/product_list')
    form_class = ProductForm


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:catalog/product_list')




class ContactView(View):
    template_name = 'catalog/contact.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
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
