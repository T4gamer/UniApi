from django.urls import path, include
from rest_framework import routers
from knox import views as knox_views
from . import views

app_name = "students"

urlpatterns = [
    path("student/main/", views.student_main_details),
    path("student/secondary/", views.student_secondary_details),
    path("register/", views.RegisterAPI.as_view(), name="register"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", knox_views.LogoutView.as_view(), name="logout"),
    path("logoutall/", knox_views.LogoutAllView.as_view(), name="logoutall"),
    path("courses/", views.CourseViewSet.as_view({"get": "list"}), name="courses"),
    path(
        "enrollment/",
        views.EnrollmentViewSet.as_view({"get": "list"}),
        name="enrollment",
    ),
    path(
        "disenroll/",
        views.EnrollmentViewSet.as_view({"get": "delete"}),
        name="enrollment",
    ),
    path(
        "enroll/",
        views.EnrollmentViewSet.as_view({"post": "create"}),
        name="signIn course",
    ),
    path("lectures/", views.LectureViewSet.as_view({"get": "list"}), name="lectures"),
    path("results/", views.ResultViewSet.as_view({"get": "list"})),
    path("results/", views.ResultViewSet.as_view({"post": "create"})),
    path("semresult/", views.SemesterResultViewSet.as_view({"post": "create","get": "list"})),
    path("semester/",views.SemesterViewSet.as_view({"get":"list"})),
    path("post/",views.PostViewSet.as_view({"get":"list"})),
    path("semester",views.SemesterViewSet.as_view({"get":"list"})),

    # path("semresult/", views.SemesterResultViewSet.as_view({})),
]
