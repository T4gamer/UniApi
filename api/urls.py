from django.urls import path
from knox import views as knox_views
from . import views

app_name = "students"

urlpatterns = [
    path("students/", views.student),
    path("students/main/", views.student_main_details),
    path("students/secondary/", views.student_secondary_details),
    path("register/", views.RegisterAPI.as_view(), name="register"),
    path("profile/", views.ManageStudentView.as_view(), name="profile"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", knox_views.LogoutView.as_view(), name="logout"),
    path("logoutall/", knox_views.LogoutAllView.as_view(), name="logoutall"),
    path("courses/", views.CourseViewSet.as_view({"get": "list"}), name="courses"),
    path(
        "enrollment/", views.EnrollmentViewSet.as_view({"get": "list"}), name="enrollment"
    ),
    path(
        "enroll/", views.EnrollmentViewSet.as_view({"post": "create"}), name="signIn course"
    ),
    path("lectures/", views.LectureViewSet.as_view({"get": "list"}), name="lectures"),
]
