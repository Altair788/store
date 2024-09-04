from django.shortcuts import render, get_object_or_404

from catalog.models import Product
from configs import FEEDBACKS_PATH
from utils import write_to_file


def products_list(request):
    products = Product.objects.all()
    context = {"products": products}
    return render(request, "main/products_list.html", context)


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {"product": product}
    return render(request, "main/product_detail.html", context)


def contact(request):
    if request.method == "POST":
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

    return render(request, "main/contact.html")
