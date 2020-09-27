from django.contrib import admin
from quiz.models import *

# Register your models here.
class QuestionInline(admin.StackedInline):
    model = Question
    extra = 10


class quizAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['title','audio']}),
    ]

    inlines = [QuestionInline]
    list_display = ('title', 'audio', 'created',)
    search_fields = ('title', )


admin.site.register(Quiz,quizAdmin)
admin.site.register(Question)
admin.site.register(Student)
