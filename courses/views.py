from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .models import Course
from .serializers import CourseSerializer
from .permissions import IsTeacher
from rest_framework.permissions import IsAuthenticated

class CourseListCreateView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    # Apply permission rules: User must be logged in AND must be a teacher.
    permission_classes = [IsAuthenticated, IsTeacher]

    def perform_create(self, serializer):
        # Automatically assign the logged-in teacher to the course.
        serializer.save(teacher=self.request.user)