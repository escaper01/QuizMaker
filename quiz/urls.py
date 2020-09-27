from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('fill_info',views.fill_info, name='fill_info'),
    path('start_quiz/<str:test_name>',views.start_quiz, name='start_quiz'),
    path('end_quiz',views.end_quiz, name='end_quiz'),
    path('grades',views.grades, name='grades'),
]