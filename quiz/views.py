from django.shortcuts import render
from quiz.models import *
from django.views import generic
from django.views.generic import CreateView, UpdateView, DeleteView
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from dateutil import parser
from datetime import datetime
import xlwt


num_of_students = 20

# Create your views here.


def export_data(request):
    # EXPORTING EXCEL SPREED SHEET

    if request.POST.get('num_row') is not '':
            num_slicer = int(request.POST.get('num_row'))
    else:
        num_slicer = num_of_students

    myQuery = Student.objects.all().order_by('-date')[:num_slicer]

    if 'excel' in request.POST:
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachement; filename = Results'+str(datetime.now())+'.xls'
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Results')
        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        columns = ['rank','first_name','last_name','serial_number',
                    'service','listening_score','reading_score','score',
                    'quiz','instructor','date']

        for col_num in range(len(columns)):
            ws.write(row_num,col_num,columns[col_num],font_style)

        font_style = xlwt.XFStyle()

        rows = myQuery.values_list('rank','first_name','last_name','serial_number',
                    'service','listening_score','reading_score','score',
                    'quiz','instructor','date')
                    
        for row in rows:
            row_num += 1

            for col_num in range(len(row)):
                ws.write(row_num,col_num,str(row[col_num]),font_style)

        wb.save(response)
        return response

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
                    last_name=request.session.get('last_name'),serial_number=request.session.get('serial_number'),
                    instructor=request.session.get('instructor'),service=request.session.get('service'),
                    rank=request.session.get('rank'),listening_score = listeningScore,
                    reading_score=readingScore, score=readingScore+listeningScore)
        s.save()
        print('go to endquiz')
        return redirect('end_quiz')
                
    print('quiz not posted')

    
    dataQuiz = {
        'quiz':quiz,
        'questions':questions
    }
    return render(request,'quiz/start_quiz.html',dataQuiz)

def end_quiz(request):
    request.session.clear()
    return render(request,'quiz/end_quiz.html')

def fill_info(request):
    quizes = Quiz.objects.all().order_by('created')
    instructors = Teacher.objects.all()
    if request.POST:
        print(request.POST)
        request.session['first_name'] = request.POST.get('first_name')
        request.session['last_name'] = request.POST.get('last_name')
        request.session['serial_number'] = request.POST.get('serial_number')
        request.session['service'] = request.POST.get('service')
        request.session['instructor'] = request.POST.get('instructor')
        request.session['rank'] = request.POST.get('rank')
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
        rank = request.POST.get('rank')
        serial_number = request.POST.get('serial_number')
        service = request.POST.get('service')
        if date == '':
            students_ls = Student.objects.filter(first_name__icontains=first_name,
                                            last_name__icontains=last_name,
                                            date__date__lte=datetime.now(),rank__icontains= rank,
                                            serial_number__icontains=serial_number,
                                            service__icontains=service).order_by('-date')
        else:
            students_ls = Student.objects.filter(first_name__icontains=first_name,
                                            last_name__icontains=last_name,
                                            date__date=parser.parse(date),rank__icontains= rank,
                                            serial_number__icontains=serial_number,
                                            service__icontains=service).order_by('-date')

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
        q = Quiz(title=request.POST.get('title'),audio=request.POST.get('audio'))
        q.save()
    return render(request,'quiz/add_quiz.html')


@login_required(login_url='login')
def add_question_quiz(request,quiz_id):
    quiz = Quiz.objects.filter(id=quiz_id)
    if request.POST:
        question = request.POST.get('question')
        answer = request.POST.get('answer')
        choice1 = request.POST.get('choice1')
        choice2 = request.POST.get('choice2')
        choice3 = request.POST.get('choice3')
        choice4 = request.POST.get('choice4')
        q = question(quiz=quiz,question=question, answer=answer, choice1=choice1, choice2=choice2, choice3=choice3, choice4=choice4)
        q.save()
    return render(request,'quiz/add_question_quiz.html')





    
    
