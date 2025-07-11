# In my_chatbot_backend/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/courses/', include('courses.urls')),
    # Add the path for our interaction endpoints
    path('api/', include('interactions.urls')),
]