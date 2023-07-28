from typing import Iterable, Optional
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.utils.translation import gettext as _

# Create your models here.


class Teacher(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


class StudentManager(BaseUserManager):
    def create_user(self, serial_number, password=None, **extra_fields):
        if not serial_number:
            raise ValueError("The Serial Number must be set")
        user = self.model(serial_number=serial_number, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, serial_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(serial_number, password, **extra_fields)


class Student(AbstractBaseUser, PermissionsMixin):
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = StudentManager()

    USERNAME_FIELD = "serial_number"
    REQUIRED_FIELDS = []

    GENDER_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
    ]

    MARITAL_CHOICES = [
        ("M", "Married"),
        ("S", "Single"),
    ]

    RESIDENCE_CHOICES = [("I", "inside"), ("O", "outside")]

    current_semester = models.ForeignKey(
        "Semester",
        related_name="current_students",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    serial_number = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    date_of_birth = models.DateField(null=True)
    place_of_birth = models.CharField(max_length=20)
    country = models.CharField(max_length=20)
    living_place = models.CharField(max_length=20)
    living_city = models.CharField(max_length=20)

    arabic_first_name = models.CharField(max_length=30)
    arabic_second_name = models.CharField(max_length=30)
    arabic_third_name = models.CharField(max_length=30)
    arabic_last_name = models.CharField(max_length=30)

    marital_status = models.CharField(max_length=1, choices=MARITAL_CHOICES)

    national_number = models.CharField(max_length=15, null=True)
    phone_number = models.IntegerField(null=True)
    credit_number = models.IntegerField(null=True)
    residence = models.CharField(max_length=1, choices=RESIDENCE_CHOICES)
    family_book_number = models.CharField(max_length=15, null=True)
    family_paper_number = models.CharField(max_length=15, null=True)
    family_serial_number = models.CharField(max_length=15, null=True)
    section = models.CharField(max_length=20)
    division = models.CharField(max_length=20)

    closest_family = models.CharField(max_length=30)
    mother_name = models.CharField(max_length=30)
    mothers_job = models.CharField(max_length=30)
    other_to_call = models.CharField(max_length=30)
    phone_number_email = models.CharField(max_length=30)

    supervisor = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.serial_number}:{self.first_name} {self.last_name}"


class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    students = models.ManyToManyField(Student, through="Enrollment")

    def __str__(self) -> str:
        return f"{self.code}:{self.name}"


class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_enrolled = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{Course.objects.get(pk=self.course.pk)}:{Student.objects.get(pk=self.student.pk)}"


class Lecture(models.Model):
    title = models.CharField(max_length=20, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    unites = models.IntegerField()
    lecture_time = models.ForeignKey("LectureTime", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.course.name}:{self.title}"


class LectureTime(models.Model):
    LECTURE_TIMES = [
        ("09:00", "9:00 AM"),
        ("10:00", "10:00 AM"),
        ("12:00", "12:00 PM"),
        ("14:00", "2:00 PM"),
    ]

    DAY_CHOICES = [
        ("SU", "SUNDAY"),
        ("MO", "MONDAY"),
        ("TU", "TUESDAY"),
        ("WE", "WEDNESDAY"),
        ("TH", "THURSDAY"),
        ("FR", "FRIDAY"),
        ("SA", "SATURDAY"),
    ]

    start_time = models.CharField(max_length=5, choices=LECTURE_TIMES)
    day = models.CharField(max_length=2, choices=DAY_CHOICES, default="MO")

    def __str__(self) -> str:
        return f"{self.start_time}:{self.get_day_display()}"


class Semester(models.Model):
    SEASON_CHOICES = [("F", "FALL"), ("S", "SPRING")]
    season = models.CharField(max_length=1, choices=SEASON_CHOICES)
    year = models.PositiveIntegerField()
    students = models.ManyToManyField(Student, related_name="semesters", blank=True)

    def __str__(self) -> str:
        return f"{self.season}{self.year}"


class Result(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    semester = models.ForeignKey(
        Semester, on_delete=models.CASCADE, related_name="results"
    )
    work_degree = models.IntegerField()
    semifinal_degree = models.IntegerField()
    final_degree = models.IntegerField()
    total_degree = models.IntegerField()

    def __str__(self) -> str:
        return f"{self.course.name}:{self.total_degree}"

    def save(self, *args, **kwargs) -> None:
        self.total_degree = self.work_degree + self.semifinal_degree + self.final_degree
        return super().save(*args, **kwargs)


class SemesterResult(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subjects = models.ManyToManyField(to=Result, default=None)
    total_degree = models.PositiveIntegerField(default=0)
    semester = models.ForeignKey(Semester , on_delete=models.CASCADE)
        
    def __str__(self) -> str:
        return f"{self.student.first_name} {self.student.last_name}"

class Post(models.Model):
    content = models.CharField(max_length=50)
    image_link = models.CharField(max_length=30)

    def __str__(self) -> str:
        return f"{self.content}"