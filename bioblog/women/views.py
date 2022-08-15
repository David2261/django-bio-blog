from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, Http404

# Create your views here.
def index(request):
	return HttpResponse("Страница приложения women")


def categories(request, cat):
	if (request.GET):
		print(request.GET)
	return HttpResponse(f"<h1>Страница приложения women</h1>\n<p>{cat}</p>")


def archive(request, year):
	if int(year) > 2022:
		return redirect('home')

	return HttpResponse(f"<h1>Архив по годам</h1>\n<p>{year}</p>")

def pageNotFound(request, exception):
	return HttpResponseNotFound('<h1>Страница не найдена</h1>')