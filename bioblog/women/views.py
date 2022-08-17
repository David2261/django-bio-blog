from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, Http404

from .models import *
from .forms import *

menu = [
	{'title': "О сайте", 'url_name': "about"},
	{'title': "Добавить статью", 'url_name': "addpage"},
	{'title': "Обратная связь", 'url_name': "contact"},
	{'title': "Войти", 'url_name': "login"},
]

# Create your views here.
def index(request):
	posts = Women.objects.all()
	context = {
		'menu': menu,
		'title': 'Main page',
		'posts': posts,
		'cat_selected': 0,
	}
	return render(request, 'women/index.html', context=context)

def show_post(request, post_slug):
	post = get_object_or_404(Women, slug=post_slug)
	context = {
		'post': post,
		'menu': menu,
		'title': post.title,
		'cat_selected': post.cat_id,
	}
	return render(request, 'women/post.html', context=context)


def show_category(request, cat_id):
	posts = Women.objects.filter(cat_id = cat_id)

	if len(posts) == 0:
		raise Http404()

	context = {
		'menu': menu,
		'title': 'Отображение по рубрикам',
		'posts': posts,
		'cat_selected': 0,
	}
	return render(request, 'women/index.html', context=context)


def about(request):
	return render(request, 'women/about.html', {'menu': menu, 'title': 'About page'})


def addpage(request):

	if request.method == 'POST':
		form = AddPostForm(request.POST)
		if form.is_valid():
		#print(form.cleaned_data)
			try:
				Women.objects.create(**form.cleaned_data)
				return redirect('home')
			except:
				form.add_error(None, 'Ошибка добавления поста')

	else:
		form = AddPostForm()

	context = {
		'form': form,
		'menu': menu,
		'title': 'Добавление статьи',
	}
	return render(request, 'women/addpage.html', context)

def contact(request):
	return HttpResponse("Обратная связь")

def login(request):
	return HttpResponse("Авторизация")

def pageNotFound(request, exception):
	return HttpResponseNotFound('<h1>Страница не найдена</h1>')