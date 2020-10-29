from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('fill_info',views.fill_info, name='fill_info'),
    path('start_quiz/<str:test_name>',views.start_quiz, name='start_quiz'),
    path('end_quiz',views.end_quiz, name='end_quiz'),
    path('grades',views.grades, name='grades'),
    path('all_quiz',views.all_quiz, name='all_quiz'),
    path('add_quiz',views.add_quiz, name='add_quiz'),
    path('choose_question/<int:quiz_id>',views.choose_question, name='choose_question'),
    path('add_question_quiz/<int:quiz_id>/<int:question_id>',views.add_or_update_question, name='add_or_update_question'),
    path('export',views.export_data, name='export_data'),
]