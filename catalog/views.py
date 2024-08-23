from django.shortcuts import render

from configs import FEEDBACKS_PATH
from utils import write_to_file


# Create your views here.
def home(request):
    return render(request, "main/home.html")


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
