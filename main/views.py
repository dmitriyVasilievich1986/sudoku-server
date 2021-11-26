from django.http.request import HttpRequest
from django.http import HttpResponse
from django.shortcuts import render


def index_view(request: HttpRequest, *args: tuple, **kwargs: dict) -> HttpResponse:
    return render(request, 'index.html')
