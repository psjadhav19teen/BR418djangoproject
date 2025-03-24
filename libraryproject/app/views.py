from django.shortcuts import render, HttpResponse
from .models import Book

# Create your views here.


# def index(req):
#     allbooks = Book.objects.all()
#     print(allbooks)
#     return HttpResponse(f"All Books:{allbooks}")


def index(req):
    allbooks = Book.objects.all()
    print(allbooks)
    context = {"myname": "ITV"}
    return render(req, "index.html", context)
