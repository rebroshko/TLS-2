from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import *
from .models import *


def index(request):
    object_list = Post.published.all()
    object_list1 = Calendar.published.all()
    paginator = Paginator(object_list, 3)  # 3 posts in each page
    Cal = Paginator(object_list1, 3)
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
        calendars = Cal.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page

        posts = paginator.page(1)
        calendars = Cal.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
        calendars = Cal.page(Cal.num_pages)
    return render(request,
                  'main/index.html',
                  {'calendars': calendars,
                   'posts': posts})


def post_detail(request, day, title):
    post = get_object_or_404(Post,
                             slug=title,
                             status='published',
                             publish__day=day)

    return render(request,
                  'main/detail.html',
                  {'post': post})


def Calendar_detail(request, day, title):
    calendars = get_object_or_404(Calendar,
                                  slug=title,
                                  status='published',
                                  publish__day=day)
    if request.method == 'POST':
        form = RecordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = RecordForm()
    return render(request,
                  'main/calendar_detail.html',
                  {'calendar': calendars,
                   'form': form})


def addfeedback(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = ContactForm()
    return render(request, 'main/addfeedback.html', {'form': form})


def Techopolis(request):
    return render(request, 'main/page1.html')


def Lager(request):
    return render(request, 'main/page3.html')


def School(request):
    return render(request, 'main/page2.html')


def Program(request):
    return render(request, 'main/program_detail.html')



