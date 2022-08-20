from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, login
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.urls import reverse_lazy

from .models import *
from .forms import *
from .utils import *


class WomenHome(DataMixin, ListView):
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
		c_def = self.get_user_context(title="Главная страница")
		# Объединение 2 словарей
		return dict(list(context.items()) + list(c_def.items()))

	# Для чтения, только для опубликованых статей
	def get_queryset(self):
		return Women.objects.filter(is_published = True).select_related('cat')


# def index(request):
# 	posts = Women.objects.all()
# 	context = {
# 		'menu': menu,
# 		'title': 'Main page',
# 		'posts': posts,
# 		'cat_selected': 0,
# 	}
# 	return render(request, 'women/index.html', context=context)


class ShowPost(DataMixin, DetailView):
	model = Women
	template_name = 'women/post.html'
	slug_url_kwarg = 'post_slug'
	# pk_url_kwarg = 'post_pk'
	context_object_name = 'post'

	def get_context_data(self, *, object_list=None, **kwargs):
		context = super().get_context_data(**kwargs)
		c_def = self.get_user_context(title=context['post'])
		return dict(list(context.items()) + list(c_def.items()))


# def show_post(request, post_slug):
# 	post = get_object_or_404(Women, slug=post_slug)
# 	context = {
# 		'post': post,
# 		'menu': menu,
# 		'title': post.title,
# 		'cat_selected': post.cat_id,
# 	}
# 	return render(request, 'women/post.html', context=context)


class WomenCategory(DataMixin, ListView):
	model = Women
	template_name = 'women/index.html'
	context_object_name = 'posts'
	# При отсутсвие каких - либо записей -> 404
	allow_empty = False

	def get_queryset(self):
		return Women.objects.filter(
				cat__slug=self.kwargs['cat_slug'],
				is_published = True).select_related('cat')

	def get_context_data(self, *, object_list=None, **kwargs):
		context = super().get_context_data(**kwargs)
		# context['title'] = 'Категория - ' + str(context['posts'][0].cat)
		# context['menu'] = menu
		# context['cat_selected'] = context['posts'][0].cat_id
		c = Category.objects.get(slug = self.kwargs['cat_slug'])
		c_def = self.get_user_context(
			title='Категория - ' + str(c.name), 
			cat_selected=c.pk
		)
		return dict(list(context.items()) + list(c_def.items()))


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
	contact_list = Women.objects.all()
	paginator = Paginator(contact_list, 3)

	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)

	context = {
		'menu': menu,
		'title': 'About page',
		'page_obj': page_obj
	}
	return render(request, 'women/about.html', context)


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
	form_class = AddPostForm
	template_name = 'women/addpage.html'
	success_url = reverse_lazy('home')
	login_url = reverse_lazy('home')
	raise_exception = True

	def get_context_data(self, *, object_list=None, **kwargs):
		context = super().get_context_data(**kwargs)
		# context['title'] = 'Добавление статьи'
		# context['menu'] = menu
		c_def = self.get_user_context(title="Добавление статьи")
		return dict(list(context.items()) + list(c_def.items()))

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


class RegisterUser(DataMixin, CreateView):
	form_class = UserCreationForm
	template_name = 'women/register.html'
	success_url = reverse_lazy('login')

	def get_context_data(self, *, object_list = None, **kwargs):
		context = super().get_context_data(**kwargs)
		c_def = self.get_user_context(title = "Регистрация")
		return dict(list(context.items()) + list(c_def.items()))

	# Авторизует пользователя сразу после регистрации
	def form_valid(self, form):
		user = form.save()
		login(self.request, user)
		return redirect('home')


class LoginUser(DataMixin, LoginView):
	form_class = LoginUserForm
	template_name = 'women/login.html'

	def get_context_data(self, *, object_list = None, **kwargs):
		context = super().get_context_data(**kwargs)
		c_def = self.get_user_context(title = 'Авторизация')
		return dict(list(context.items()) + list(c_def.items()))

	def get_success_url(self):
		return reverse_lazy('home')


def logout_user(request):
	logout(request)
	return redirect('login')

def pageNotFound(request, exception):
	return HttpResponseNotFound('<h1>Страница не найдена</h1>')