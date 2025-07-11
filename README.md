Chatbot LMS - Backend API Documentation
This document provides instructions on how to use the backend API for the Learning Management System.

Authentication Endpoints
1. User Registration
Creates a new user account with a specific role.

URL: /api/auth/register/

Method: POST

Auth: None required.

Request Body:

JSON

{
    "username": "new_user",
    "email": "user@example.com",
    "password": "a_strong_password",
    "role": "student"
}
Success Response (201 Created):

JSON

{
    "user": {
        "id": 1,
        "username": "new_user",
        "role": "student"
    },
    "message": "User created successfully."
}
2. User Login
Logs in an existing user and returns authentication tokens.

URL: /api/auth/login/

Method: POST

Auth: None required.

Request Body:

JSON

{
    "username": "existing_user",
    "password": "their_password"
}
Success Response (200 OK):

JSON

{
    "refresh": "eyJhbGciOiJIUzI1Ni...",
    "access": "eyJhbGciOiJIUzI1Ni..."
}
3. Get Current User Profile
Fetches the profile information of the currently logged-in user.

URL: /api/auth/me/

Method: GET

Auth: Bearer Token (Any User) required.

Success Response (200 OK):

JSON

{
    "id": 1,
    "username": "current_user",
    "email": "user@example.com",
    "first_name": "",
    "last_name": "",
    "role": "student"
}
Course & Enrollment Endpoints
1. List All Courses
Retrieves a list of all courses available.

URL: /api/courses/

Method: GET

Auth: Bearer Token (Any User) required.

Success Response (200 OK):

JSON

[
    {
        "id": 1,
        "title": "History of Ancient Rome",
        "description": "A course by a teacher.",
        "created_at": "...",
        "teacher": 2
    }
]
2. Create a Course
Creates a new course.

URL: /api/courses/

Method: POST

Auth: Bearer Token (Teacher Only) required.

Request Body:

JSON

{
    "title": "New Course Title",
    "description": "A description for the course."
}
Success Response (201 Created):

JSON

{
    "id": 2,
    "title": "New Course Title",
    "description": "A description for the course.",
    "created_at": "...",
    "teacher": 3
}
3. Enroll in a Course
Enrolls the current student in a specific course.

URL: /api/courses/<course_id>/enroll/

Method: POST

Auth: Bearer Token (Student Only) required.

Success Response (201 Created):

JSON

{
    "id": 1,
    "course": 1,
    "student": 2,
    "enrolled_at": "..."
}
Interaction Endpoints
1. Submit a Quiz
Submits answers for a specific quiz and gets a score.

URL: /api/quizzes/<quiz_id>/submit/

Method: POST

Auth: Bearer Token (Enrolled Student Only) required.

Request Body:

JSON

{
    "answers": [
        {
            "question": 1,
            "selected_choice": 2
        },
        {
            "question": 2,
            "selected_choice": 5
        }
    ]
}
Success Response (201 Created):

JSON

{
    "id": 1,
    "quiz": 1,
    "score": 100.0,
    "submitted_at": "..."
}
2. Send a Chat Message
Sends a message within a lesson and receives a simulated LLM response.

URL: /api/lessons/<lesson_id>/chat/

Method: POST

Auth: Bearer Token (Enrolled Student Only) required.

Request Body:

JSON

{
    "message_text": "Can you explain this topic further?"
}
Success Response (201 Created):

JSON

{
    "id": 1,
    "lesson": 1,
    "student": 2,
    "message_text": "Can you explain this topic further?",
    "response_text": "This is a simulated response to: 'Can you explain this topic further?'",
    "sent_at": "..."
}
