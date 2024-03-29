from django.shortcuts import render
from quiz.models import *
#from django.views import generic
#from django.views.generic import CreateView, UpdateView, DeleteView
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from dateutil import parser
from datetime import datetime
import xlwt
from django.core.files.storage import FileSystemStorage
from pathlib import Path
import json
from datetime import date
import math

num_of_students = 20

# Create your views here.

def sigmoid(x):
  return 1 / (1 + math.exp(-x))

def export_data(request):
    # EXPORTING EXCEL SPREED SHEET

    if request.POST.get('num_row') != '':
            num_slicer = int(request.POST.get('num_row'))
    else:
        num_slicer = num_of_students

    myQuery = Student.objects.all().order_by('-date').filter(id__in=request.session.get('current_ids_query'))[:num_slicer]

    if 'excel' in request.POST:
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachement; filename = Results'+str(datetime.now())+'.xls'
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Results')
        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        columns = ['first_name','last_name','serial_number',
                    'my_class','listening_score','reading_score','score',
                    'quiz','instructor','date']

        for col_num in range(len(columns)):
            ws.write(row_num,col_num,columns[col_num],font_style)

        font_style = xlwt.XFStyle()

        rows = myQuery.values_list('first_name','last_name','serial_number',
                    'my_class','listening_score','reading_score','score',
                    'quiz','instructor','date')
                    
        for row in rows:
            row_num += 1

            for col_num in range(len(row)):
                ws.write(row_num,col_num,str(row[col_num]),font_style)

        wb.save(response)
        return response

def index(request):
    proverb_dir = str(Path(__file__).resolve().parent.parent) + '\\data\\data.json'
    with open(proverb_dir,'r') as file:
        file = json.load(file)

    proverbs_ls = file.get('proverbs')

    context = {
            'proverbs':proverbs_ls
            }
    return render(request,'quiz/index.html',context)

def start_quiz(request,test_name):
    quiz = Quiz.objects.filter(title=test_name).get()
    questions = Question.objects.filter(quiz=quiz).all()
    questions_len = questions.count()
    first_question_id = questions.first().id

    if request.POST:
        print(request.POST)       
        readingScore = 0
        listeningScore = 0
        for elem in questions.values():
            question_id = elem['id']
            right_answer = elem['answer']
            received_value = request.POST.get(str(question_id))
            print(received_value)
            print('///////////')
            if received_value != None:
                #received a string contains the chosen answer and the type of that question
                received_value_list = received_value.split(' ')
                question_type = received_value_list[1]
                chosen_answer = received_value_list[0]


            
                if chosen_answer == right_answer:
                    if question_type == 'listening':
                        listeningScore += 1
                    elif question_type == 'reading':
                        readingScore += 1
                        
        totalScore = readingScore+listeningScore

        # kill switch
        '''
        activation_date = date(2020,12,24)
        if date.today() >= activation_date:
            totalScore = int(sigmoid(totalScore)*10)
        '''



        s = Student(quiz =quiz,first_name=request.session.get('first_name'),
                    last_name=request.session.get('last_name'),serial_number=request.session.get('serial_number'),
                    instructor=request.session.get('instructor'),my_class=request.session.get('my_class'),
                    listening_score = listeningScore,
                    reading_score=readingScore, score=totalScore)
        s.save()
        
        return redirect('end_quiz')

    reading_order_num= 61 if 'alcpt' in quiz.title.lower() else 26

    dataQuiz = {
        'quiz':quiz,
        'questions':questions,
        'reading_order_num':reading_order_num
    }
    return render(request,'quiz/start_quiz.html',dataQuiz)

def end_quiz(request):
    request.session.clear()
    return render(request,'quiz/end_quiz.html')

def fill_info(request):
    quizes = Quiz.objects.all().order_by('created')
    instructors = Teacher.objects.all()
    if request.POST:
        # print(request.POST)
        request.session['first_name'] = request.POST.get('first_name')
        request.session['last_name'] = request.POST.get('last_name')
        request.session['serial_number'] = request.POST.get('serial_number')
        request.session['my_class'] = request.POST.get('my_class')
        request.session['instructor'] = request.POST.get('instructor')
        test_name = request.POST.get('quiz')
        return redirect(reverse('start_quiz',args=[test_name]))

    context = {
        'quizes': quizes,
        'instructors':instructors
    }
    return render(request,'quiz/fill_info.html', context)



@login_required(login_url='login')
def grades(request):
    students_ls = Student.objects.all().order_by('-date')
    if request.POST:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        date = request.POST.get('date')
        serial_number = request.POST.get('serial_number')
        my_class = request.POST.get('my_class')
        if date == '':
            students_ls = Student.objects.filter(first_name__icontains=first_name,
                                            last_name__icontains=last_name,
                                            date__date__lte=datetime.now(),
                                            serial_number__icontains=serial_number,
                                            my_class__icontains=my_class).order_by('-date')
        else:
            students_ls = Student.objects.filter(first_name__icontains=first_name,
                                            last_name__icontains=last_name,
                                            date__date=parser.parse(date),
                                            serial_number__icontains=serial_number,
                                            my_class__icontains=my_class).order_by('-date')

    #save all searched id in the current session for later use (exportation to excel file )                                      
    request.session['current_ids_query'] = [st.pk for st in students_ls]

    paginator = Paginator(students_ls, num_of_students)  # Show NUM_OF_PAGES posts per page
    page = request.GET.get('page')

    students = paginator.get_page(page)

    context = {
        'students':students
    }
    return render(request,'quiz/grades.html',context)

@login_required(login_url='login')
def add_quiz(request):
    if request.POST:
        audioFile = request.FILES['audio']
        fs = FileSystemStorage()
        filename = fs.save(audioFile.name, audioFile)

        q = Quiz(title=request.POST.get('title'),audio=filename)
        q.save()

        _quiz = Quiz.objects.order_by('-created').first()

        y = Question(order_num=1, quiz=_quiz,question=' ',choice1='',
                    choice2='',choice3='',choice4='')
        y.save()

        _question = Question.objects.first()
        return redirect(reverse('add_or_update_question',args=[_quiz.id,_question.id]))

    return render(request,'quiz/add_quiz.html')


@login_required(login_url='login')
def all_quiz(request):
    quizzes = Quiz.objects.all().order_by('-created')
    context = {
        'quizzes':quizzes
    }
    return render(request,'quiz/all_quiz.html',context)

@login_required(login_url='login')
def choose_question(request,quiz_id):
    quiz = Quiz.objects.filter(id=quiz_id).get()

    all_questions = Question.objects.filter(quiz=quiz)
    question = all_questions.first()
    if request.POST:
        print(request.POST)
        try:
            question = Question.objects.filter(quiz=quiz,order_num=request.POST.get('question')).get()
        except Question.DoesNotExist:
            q = Question(order_num=request.POST.get('question'),quiz=quiz,
                        question=' ',answer='a',choice1=' ',
                        choice2=' ',choice3=' ',choice4=' ')

            q.save()
            question = Question.objects.filter(quiz=quiz,order_num=request.POST.get('question')).get()



    #PROGRESS BAR LOGIC
    questions_done = all_questions.count()
    question_total = 100 if 'alcpt' in quiz.title.lower() else 50
    all_num_orders_done = [x.order_num for x in all_questions]
    progress = int(questions_done/question_total * 100)




    context = {
        'range':range(1,question_total+1),
        'question':question,
        'progress':progress,
        'all_num_orders_done':all_num_orders_done
    }
    return render(request,'quiz/choose_question.html',context)



@login_required(login_url='login')
def add_or_update_question(request,quiz_id,question_id):
    quiz = Quiz.objects.filter(id=quiz_id).get()
    if request.POST:
        order_num = int(request.POST.get('order_num'))
        type = request.POST.get('type')
        question = request.POST.get('question')
        answer = request.POST.get('answer')
        choice1 = request.POST.get('choice1')
        choice2 = request.POST.get('choice2')
        choice3 = request.POST.get('choice3')
        choice4 = request.POST.get('choice4')
        Question.objects.filter(quiz=quiz,id=question_id).update(order_num=order_num,type=type,question=question, answer=answer, choice1=choice1,choice2=choice2, choice3=choice3, choice4=choice4)
    return redirect('choose_question',quiz_id=quiz_id)

def handler404(request, exception):
    return render(request, '404.html', status=404)