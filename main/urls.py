from . import views
from django.urls import path


app_name = 'Main'
urlpatterns = [
    path('', views.index, name='home'),
    path('addfeedback/', views.addfeedback, name='addfeedback'),
    path('school/', views.School, name='page2'),
    path('technopolis/', views.Techopolis, name='page1'),
    path('lager/', views.Lager, name='page3'),
    path('program_detail/', views.Program, name='program'),
    path('<int:day>/<slug:title>/',
         views.post_detail,
         name='post_detail'),
    path('<slug:title>/<int:day>/',
         views.Calendar_detail,
         name='Calendar_detail'),
]
