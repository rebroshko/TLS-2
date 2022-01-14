"""djangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from pages.views import *
from django.conf.urls.static import static


urlpatterns = [
    path('', include('main.urls', namespace='Main')),
    path('book/', AuthView.as_view(), name='login'),
    path('admin/', admin.site.urls),
    path('teacher/', TeacherPageView.as_view(), name='teacher'),
    path('child/', ChildPageView.as_view(), name='child'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('api/getGroups', GroupsApiView.as_view()),
    path('api/getPeriod', PeriodApiView.as_view()),
    path('api/getSubGroups', SubGroupsApiView.as_view()),
    path('api/getSubjects', SubjectsApiView.as_view()),
    path('api/getTable', TableApiView.as_view()),
    path('api/setMark', SetMarkView.as_view()),
    path('api/setLesson', SetLessonView.as_view()),
    path('api/getMark', MarkApiView.as_view())
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
