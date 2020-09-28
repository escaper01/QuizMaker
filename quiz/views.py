from django.shortcuts import render
from quiz.models import *
from django.views import generic
from django.views.generic import CreateView, UpdateView, DeleteView
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from dateutil import parser
from datetime import datetime

NUM_OF_POSTS = 10

# Create your views here.

def index(request):
    return render(request,'quiz/index.html')

def start_quiz(request,test_name):

    quiz = Quiz.objects.filter(title=test_name).get()
    questions = Question.objects.filter(quiz=quiz).all()
    questions_len = questions.count()
    first_question_id = questions.first().id
    #last index of the part I minus one
    index_target = 2
    middle_question_id = first_question_id + index_target

    if request.POST:
        readingScore = 0
        listeningScore = 0
        for elem in questions.values():
            question_id = elem['id']
            right_answer = elem['answer']
            chosen_answer = request.POST.get(str(question_id))
            
            if chosen_answer == right_answer and question_id <= middle_question_id:
                listeningScore += 1

            elif chosen_answer == right_answer and question_id > middle_question_id:
                readingScore += 1

        s = Student(quiz =quiz,first_name=request.session.get('first_name'),
                    last_name=request.session.get('last_name'),listening_score = listeningScore,
                    reading_score=readingScore, score=readingScore+listeningScore)
        s.save()
        return redirect('end_quiz')
                


    
    dataQuiz = {
        'quiz':quiz,
        'questions':questions
    }
    return render(request,'quiz/start_quiz.html',dataQuiz)

def end_quiz(request):
    return render(request,'quiz/end_quiz.html')

def fill_info(request):
    if request.POST:
        request.session['first_name'] = request.POST.get('first_name')
        request.session['last_name'] = request.POST.get('last_name')
        test_name = request.POST.get('quiz')
        return redirect(reverse('start_quiz',args=[test_name]))
    return render(request,'quiz/fill_info.html')



@login_required(login_url='login')
def grades(request):
    students_ls = Student.objects.all().order_by('-date')
    if request.POST:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        date = request.POST.get('date')
        if date == '':
            students_ls = Student.objects.filter(first_name__icontains=first_name,
                                            last_name__icontains=last_name,
                                            date__date__lte=datetime.now()).order_by('-date')
        else:
            students_ls = Student.objects.filter(first_name__icontains=first_name,
                                            last_name__icontains=last_name,
                                            date__date=parser.parse(date)).order_by('-date')

    paginator = Paginator(students_ls, NUM_OF_POSTS)  # Show NUM_OF_PAGES posts per page
    page = request.GET.get('page')

    students = paginator.get_page(page)

    context = {
        'students':students
    }
    return render(request,'quiz/grades.html',context)