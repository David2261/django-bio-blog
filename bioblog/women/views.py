from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, Http404


from .models import *


menu = ["About site", "Add article", "FeedBack", "Login"]

# Create your views here.
def index(request):
	posts = Women.objects.all()
	return render(request, 'women/index.html', {'menu': menu, 'title': 'Main page', 'posts': posts})


def about(request):
	return render(request, 'women/about.html', {'menu': menu, 'title': 'About page'})


def categories(request, cat):
	if (request.GET):
		print(request.GET)
	return HttpResponse(f"<h1>Страница по категориям</h1>\n<p>{cat}</p>")


def archive(request, year):
	if int(year) > 2022:
		return redirect('home')

	return HttpResponse(f"<h1>Архив по годам</h1>\n<p>{year}</p>")


def pageNotFound(request, exception):
	return HttpResponseNotFound('<h1>Страница не найдена</h1>')