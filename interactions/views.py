from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from courses.models import Course, Quiz, QuizChoice # Import Quiz and QuizChoice
from .models import Enrollment, QuizSubmission, SubmissionAnswer, ChatMessage
from .serializers import EnrollmentSerializer, QuizSubmissionSerializer, ChatMessageSerializer # Import QuizSubmissionSerializer
from .permissions import IsStudent, IsEnrolledStudent, IsEnrolledInCourseForLesson# Import IsEnrolledStudent

# ... (EnrollmentCreateView code is already here) ...
class EnrollmentCreateView(generics.CreateAPIView):
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated, IsStudent]

    def create(self, request, *args, **kwargs):
        course_id = self.kwargs.get('course_id')
        try:
            course = Course.objects.get(pk=course_id)
        except Course.DoesNotExist:
            return Response({"detail": "Course not found."}, status=status.HTTP_404_NOT_FOUND)

        if Enrollment.objects.filter(student=request.user, course=course).exists():
            return Response({"detail": "You are already enrolled in this course."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data={'course': course.id})
        serializer.is_valid(raise_exception=True)
        serializer.save(student=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# ADD THE NEW VIEW CLASS BELOW
class QuizSubmissionCreateView(generics.CreateAPIView):
    serializer_class = QuizSubmissionSerializer
    # Apply our new advanced permission
    permission_classes = [IsAuthenticated, IsEnrolledStudent]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        quiz_id = self.kwargs.get('quiz_id')
        answers_data = serializer.validated_data.pop('answers')

        # --- Score Calculation Logic ---
        total_questions = Quiz.objects.get(pk=quiz_id).questions.count()
        correct_answers = 0
        for answer_data in answers_data:
            choice = answer_data['selected_choice']
            if choice.is_correct:
                correct_answers += 1

        score = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
        # --- End of Score Calculation ---

        # Find the enrollment record for the student and course
        quiz = Quiz.objects.get(pk=quiz_id)
        enrollment = Enrollment.objects.get(student=request.user, course=quiz.lesson.course)

        # Create the QuizSubmission instance
        submission = QuizSubmission.objects.create(
            enrollment=enrollment,
            quiz_id=quiz_id,
            score=score
        )

        # Create the related SubmissionAnswer instances
        for answer_data in answers_data:
            SubmissionAnswer.objects.create(
                submission=submission,
                question=answer_data['question'],
                selected_choice=answer_data['selected_choice']
            )

        # Manually serialize the response to include the score
        response_serializer = self.get_serializer(submission)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    
# ADD THE NEW VIEW CLASS
class ChatView(generics.CreateAPIView):
    """
    An endpoint for students to post chat messages in a lesson.
    """
    serializer_class = ChatMessageSerializer
    permission_classes = [IsAuthenticated, IsEnrolledInCourseForLesson]

    def perform_create(self, serializer):
        lesson_id = self.kwargs.get('lesson_id')
        
        # --- Simulate LLM Response (Placeholder) ---
        # Naufal will replace this with a real call to the LLM API later.
        student_message = serializer.validated_data.get('message_text')
        llm_response = f"This is a simulated response to: '{student_message}'"
        # --- End of Simulation ---

        # Save the full chat message with the simulated response
        serializer.save(
            student=self.request.user,
            lesson_id=lesson_id,
            response_text=llm_response
        )