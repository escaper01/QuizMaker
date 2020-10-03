from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('fill_info',views.fill_info, name='fill_info'),
    path('start_quiz/<str:test_name>',views.start_quiz, name='start_quiz'),
    path('end_quiz',views.end_quiz, name='end_quiz'),
    path('grades',views.grades, name='grades'),
    path('add_quiz',views.add_quiz, name='add_quiz'),
    path('add_question_quiz/<int:quiz_id>',views.add_question_quiz, name='add_question_quiz'),
    path('export',views.export_data, name='export_data'),
]