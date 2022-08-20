from django.db.models import Count

from .models import *


menu = [
	{'title': "О сайте", 'url_name': "about"},
	{'title': "Добавить статью", 'url_name': "addpage"},
	{'title': "Обратная связь", 'url_name': "contact"},
]


class DataMixin:
	paginate_by = 5
	# Формирует контекст для шаблона.
	def get_user_context(self, **kwargs):
		context = kwargs
		# Отображает, только те категории, в которых
		# 						есть хотя бы 1 статья.
		cats = Category.objects.annotate(Count('women'))
		# Если пользователь не авторизован,
		# 		то страница "Добавить статью" не отображается.
		user_menu = menu.copy()
		if not self.request.user.is_authenticated:
			user_menu.pop(1)
		context['menu'] = user_menu
		context['cats'] = cats
		if 'cat_selected' not in context:
			context['cat_selected'] = 0
		return context
