# ForeignKey - Для связей Many to One (Поля отношений)
# 	ForeignKey(
# 		<ссылка на первичную модель>,
# 		on_delete=<ограничения при удалении>
# 	)
# ManyToManyField - Для связей Many to Many (многие ко многим)
# OneToOneField - Для связей One to One (один к одному)

from django.db import models
from django.urls import reverse


class Women(models.Model):
	title = models.CharField(max_length=255, blank=False, verbose_name="Заголовок")
	slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
	content = models.TextField(blank=True, verbose_name="Текст статьи")
	photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name="Фото")
	time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
	time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")
	is_published = models.BooleanField(default=True, verbose_name="Публикация")
	cat = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name="Категория")

	# Заголовок текущей записи
	def __str__(self):
		return self.title

	# Формирует маршрут к конкретной записи
	def get_absolute_url(self):
		return reverse("post", kwargs={'post_slug': self.slug})

	class Meta:
		verbose_name = 'Женщины'
		verbose_name_plural = 'Известные женщины'
		ordering = ['-time_create', 'title']


class Category(models.Model):
	name = models.CharField(max_length=100, db_index=True, verbose_name="Категория")
	slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse("category", kwargs={'cat_id': self.pk})

	class Meta:
		verbose_name = 'Категория'
		verbose_name_plural = 'Категории'
		ordering = ['id']
		

