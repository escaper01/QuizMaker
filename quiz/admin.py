from django.contrib import admin
from quiz.models import *

# Register your models here.
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id','order_num','quiz','question','type','choice1','choice2','choice3','choice4','answer')
    list_editable = ('type','answer')

class QuestionInline(admin.StackedInline):
    model = Question
    extra = 10


class quizAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['title','audio']}),
    ]

    inlines = [QuestionInline]
    list_display = ('id','title', 'audio', 'created',)
    search_fields = ('title', )


class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name','last_name','serial_number','instructor','my_class','listening_score','reading_score','score','date',)

admin.site.register(Quiz,quizAdmin)
admin.site.register(Question,QuestionAdmin)
admin.site.register(Student,StudentAdmin)
admin.site.register(Teacher)


