from rest_framework.permissions import BasePermission
from .models import Enrollment
from courses.models import Quiz
from courses.models import GeneratedLesson


class IsStudent(BasePermission):
    """
    Allows access only to users with the 'student' role.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'student'
    
# ADD THE NEW PERMISSION CLASS BELOW
class IsEnrolledStudent(BasePermission):
    """
    Allows access only to students who are enrolled in the course
    associated with the quiz.
    """
    def has_permission(self, request, view):
        # First, check if the user is a student
        if not (request.user and request.user.is_authenticated and request.user.role == 'student'):
            return False

        # Get the quiz_id from the URL
        quiz_id = view.kwargs.get('quiz_id')
        if not quiz_id:
            return False

        try:
            # Find the course this quiz belongs to
            quiz = Quiz.objects.get(pk=quiz_id)
            course = quiz.lesson.course
            # Check if an enrollment record exists for this student and course
            return Enrollment.objects.filter(student=request.user, course=course).exists()
        except Quiz.DoesNotExist:
            return False
        
class IsEnrolledInCourseForLesson(BasePermission):
    """
    Allows access only to students who are enrolled in the course
    that the lesson belongs to.
    """
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated and request.user.role == 'student'):
            return False

        lesson_id = view.kwargs.get('lesson_id')
        if not lesson_id:
            return False

        try:
            lesson = GeneratedLesson.objects.get(pk=lesson_id)
            # Check if an enrollment record exists for this student and the lesson's course
            return Enrollment.objects.filter(student=request.user, course=lesson.course).exists()
        except GeneratedLesson.DoesNotExist:
            return False