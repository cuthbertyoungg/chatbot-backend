from rest_framework import serializers
from .models import Enrollment, QuizSubmission, SubmissionAnswer
from .models import ChatMessage 

class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ['id', 'course', 'student', 'enrolled_at']
        read_only_fields = ['student', 'enrolled_at']

# This serializer handles a single answer from the student
class SubmissionAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmissionAnswer
        fields = ['question', 'selected_choice']

# This serializer handles the entire quiz submission
class QuizSubmissionSerializer(serializers.ModelSerializer):
    # This is a nested serializer. It expects a list of answer objects.
    answers = SubmissionAnswerSerializer(many=True, write_only=True)

    class Meta:
        model = QuizSubmission
        # The 'answers' field is for input, the others are for output
        fields = ['id', 'quiz', 'score', 'submitted_at', 'answers']
        read_only_fields = ['quiz','score', 'submitted_at']

    # We will add a create() method here later to calculate the score
    
class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        # We only need the student's message as input
        fields = ['id', 'lesson', 'student', 'message_text', 'response_text', 'sent_at']
        read_only_fields = ['id', 'lesson', 'student', 'response_text', 'sent_at']