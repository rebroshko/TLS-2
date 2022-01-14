from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.conf import settings
from django.utils.timezone import now


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish')
    cover = models.ImageField(upload_to='images/')
    body = models.TextField()
    short = models.TextField(max_length=90)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='draft')
    objects = models.Manager() # The default manager.
    published = PublishedManager() # Our custom manager.

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('Main:post_detail',
                       args=[self.publish.day,
                             self.slug])


class Contact(models.Model):
    name = models.CharField(max_length=100, verbose_name="Введите имя")
    phone = models.CharField(max_length=70, verbose_name="Номер телефона")
    email = models.EmailField(max_length=150, verbose_name="Email")
    message = models.CharField( max_length=2000, verbose_name="Комментарий или вопрос")
    time_create = models.DateTimeField(default=now, editable=False)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'
        ordering = ['-time_create', 'name']


class CalendarManager(models.Manager):
    def get_queryset(self):
        return super(CalendarManager, self).get_queryset().filter(status='published')


class Calendar(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=90, verbose_name="Заголовок")
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish')
    body = models.TextField(verbose_name="Текст для статьи")
    publish = models.DateTimeField(default=timezone.now)
    date_go = models.DateTimeField(default=timezone.now, verbose_name="Когда будет мероприятие")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='draft', verbose_name="Выбрать паблиш если нужно опубликовать или драфт если необходимо скрыть")
    objects = models.Manager() # The default manager.
    published = CalendarManager() # Our custom manager.

    class Meta:
        verbose_name = 'Ближайшие события'
        verbose_name_plural = 'Ближайшие события'
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('Main:Calendar_detail',
                       args=[self.slug,
                             self.publish.day])


class Record(models.Model):
    choice_Rec = models.ForeignKey(Calendar, on_delete=models.CASCADE, verbose_name="Cобытие")
    name = models.CharField(max_length=100, verbose_name="Введите имя")
    phone = models.CharField(max_length=70, verbose_name="Номер телефона или email")
    message = models.CharField(max_length=2000, verbose_name="Комментарий или вопрос")
    time_create = models.DateTimeField(default=now, editable=False)

    def __str__(self):
        return f"{self.name} - {self.choice_Rec}"

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    class Meta:
        verbose_name = 'Запись к событию'
        verbose_name_plural = 'Записи к событиям'
        ordering = ['-time_create', 'name']