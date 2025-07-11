# Di dalam courses/models.py

from django.db import models
from django.conf import settings

class Course(models.Model):
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    TARGET_AGE_CHOICES = [
        ('7-12', '7-12 years'),
        ('12-16', '12-16 years'),
        ('17-22', '17 -22 years'),
        ('23-30', '23-30 years'),
    ]
    TEACHING_STYLE_CHOICES = [
        ('formal', 'Formal & Structured'),
        ('conversational', 'Casual & Conversational'),
        ('story-based', 'Story-based & Narrative'),
    ]
    target_age = models.CharField(max_length=10, choices=TARGET_AGE_CHOICES, blank=True)
    teaching_style = models.CharField(max_length=20, choices=TEACHING_STYLE_CHOICES, blank=True)

    def __str__(self):
        return self.title

class SourceMaterial(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    file = models.FileField(upload_to='source_materials/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        import os
        return os.path.basename(self.file.name)

class GeneratedLesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    order = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.course.title} - Lesson {self.order}: {self.title}"

class Quiz(models.Model):
    lesson = models.OneToOneField(GeneratedLesson, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

class QuizQuestion(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)
    question_text = models.TextField()
    order = models.PositiveIntegerField()
    class Meta:
        # This rule says the combination of 'quiz' and 'order' must be unique.
        unique_together = ('quiz', 'order')

    def __str__(self):
        return f"Q{self.order}: {self.question_text[:50]}..."

class QuizChoice(models.Model):
    question = models.ForeignKey(QuizQuestion, related_name='choices', on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text