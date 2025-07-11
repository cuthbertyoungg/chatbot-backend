from django.urls import path
from .views import CourseListCreateView
from interactions.views import EnrollmentCreateView


urlpatterns = [
    path('', CourseListCreateView.as_view(), name='course-list-create'),
    path('<int:course_id>/enroll/', EnrollmentCreateView.as_view(), name='course-enroll'),

]