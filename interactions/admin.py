from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Enrollment, ChatMessage, QuizSubmission

admin.site.register(Enrollment)
admin.site.register(ChatMessage)
admin.site.register(QuizSubmission)