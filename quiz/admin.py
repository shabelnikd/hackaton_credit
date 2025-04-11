from django.contrib import admin
from .models import Question, Answer

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 1  # Количество пустых строк для добавления новых ответов

class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text', 'correct_answer']
    inlines = [AnswerInline]

admin.site.register(Question, QuestionAdmin)

