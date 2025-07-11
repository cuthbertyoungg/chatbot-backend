# In interactions/urls.py
from django.urls import path
from .views import QuizSubmissionCreateView, ChatView

urlpatterns = [
    # The URL for a student to submit a specific quiz
    path('quizzes/<int:quiz_id>/submit/', QuizSubmissionCreateView.as_view(), name='quiz-submit'),
    path('lessons/<int:lesson_id>/chat/', ChatView.as_view(), name='lesson-chat'),
]