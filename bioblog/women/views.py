from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from .models import *
from .forms import *


menu = [
	{'title': "О сайте", 'url_name': "about"},
	{'title': "Добавить статью", 'url_name': "addpage"},
	{'title': "Обратная связь", 'url_name': "contact"},
	{'title': "Войти", 'url_name': "login"},
]


class WomenHome(ListView):
	model = Women
	template_name = 'women/index.html'
	# Название переменной, которую можно исп-ть в шаблоне
	context_object_name = 'posts'
	# Для статических данных
	# extra_context = {'title': 'Главная страница'}

	# Для динамических данных
	def get_context_data(self, *, object_list=None, **kwargs):
		# Обращение к базовому классу ListView
		# 		и взять существующий контекст.
		context = super().get_context_data(**kwargs)
		context['menu'] = menu
		context['title'] = 'Главная страница'
		context['cat_selected'] = 0
		return context

	# Для чтения, только для опубликованых статей
	def get_queryset(self):
		return Women.objects.filter(is_published = True)


# def index(request):
# 	posts = Women.objects.all()
# 	context = {
# 		'menu': menu,
# 		'title': 'Main page',
# 		'posts': posts,
# 		'cat_selected': 0,
# 	}
# 	return render(request, 'women/index.html', context=context)


class ShowPost(DetailView):
	model = Women
	template_name = 'women/post.html'
	slug_url_kwarg = 'post_slug'
	# pk_url_kwarg = 'post_pk'
	context_object_name = 'post'

	def get_context_data(self, *, object_list=None, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = context['post']
		context['menu'] = menu
		return context


# def show_post(request, post_slug):
# 	post = get_object_or_404(Women, slug=post_slug)
# 	context = {
# 		'post': post,
# 		'menu': menu,
# 		'title': post.title,
# 		'cat_selected': post.cat_id,
# 	}
# 	return render(request, 'women/post.html', context=context)


class WomenCategory(ListView):
	model = Women
	template_name = 'women/index.html'
	context_object_name = 'posts'
	# При отсутсвие каких - либо записей -> 404
	allow_empty = False

	def get_queryset(self):
		return Women.objects.filter(
				cat__slug=self.kwargs['cat_slug'],
				is_published = True)

	def get_context_data(self, *, object_list=None, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Категория - ' + str(context['posts'][0].cat)
		context['menu'] = menu
		context['cat_selected'] = context['posts'][0].cat_id
		return context


# def show_category(request, cat_id):
# 	posts = Women.objects.filter(cat_id = cat_id)

# 	if len(posts) == 0:
# 		raise Http404()

# 	context = {
# 		'menu': menu,
# 		'title': 'Отображение по рубрикам',
# 		'posts': posts,
# 		'cat_selected': 0,
# 	}
# 	return render(request, 'women/index.html', context=context)


def about(request):
	return render(request, 'women/about.html', {'menu': menu, 'title': 'About page'})


class AddPage(CreateView):
	form_class = AddPostForm
	template_name = 'women/addpage.html'
	success_url = reverse_lazy('home')

	def get_context_data(self, *, object_list=None, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Добавление статьи'
		context['menu'] = menu
		return context

# def addpage(request):

# 	if request.method == 'POST':
# 		form = AddPostForm(request.POST)
# 		if form.is_valid():
# 		#print(form.cleaned_data)
# 			try:
# 				form.save()
# 				return redirect('home')
# 			except:
# 				form.add_error(None, 'Ошибка добавления поста')

# 	else:
# 		form = AddPostForm()

# 	context = {
# 		'form': form,
# 		'menu': menu,
# 		'title': 'Добавление статьи',
# 	}
# 	return render(request, 'women/addpage.html', context)


def contact(request):
	return HttpResponse("Обратная связь")


def login(request):
	return HttpResponse("Авторизация")


def pageNotFound(request, exception):
	return HttpResponseNotFound('<h1>Страница не найдена</h1>')