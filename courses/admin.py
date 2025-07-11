from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Course, GeneratedLesson, Quiz, QuizQuestion, QuizChoice

admin.site.register(Course)
admin.site.register(GeneratedLesson)
admin.site.register(Quiz)
admin.site.register(QuizQuestion)
admin.site.register(QuizChoice)